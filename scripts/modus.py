#!/usr/bin/env python3
"""Modus themes port management CLI."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.common import contrast as contrast_utils
from scripts.common import io
from scripts.common import paths
from scripts.common import registry as registry_utils
from scripts.common import template as template_utils
from scripts.common import theme_ops

PALETTE_SOURCE = "https://protesilaos.com/emacs/modus-themes-colors"
SHIKI_THEME_FORMAT = "shiki-theme"
HEX_COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
SHIKI_ANSI_COLOR_KEYS = (
    "terminal.ansiBlack",
    "terminal.ansiRed",
    "terminal.ansiGreen",
    "terminal.ansiYellow",
    "terminal.ansiBlue",
    "terminal.ansiMagenta",
    "terminal.ansiCyan",
    "terminal.ansiWhite",
    "terminal.ansiBrightBlack",
    "terminal.ansiBrightRed",
    "terminal.ansiBrightGreen",
    "terminal.ansiBrightYellow",
    "terminal.ansiBrightBlue",
    "terminal.ansiBrightMagenta",
    "terminal.ansiBrightCyan",
    "terminal.ansiBrightWhite",
)
SHIKI_COLOR_KEYS = {
    "editor.foreground",
    "editor.background",
    *SHIKI_ANSI_COLOR_KEYS,
}
SHIKI_THEME_KEYS = {
    "name",
    "displayName",
    "type",
    "fg",
    "bg",
    "colors",
    "tokenColors",
}
SHIKI_TOKEN_RULE_KEYS = {"name", "scope", "settings"}
SHIKI_TOKEN_SETTING_KEYS = {"foreground", "background", "fontStyle"}
SHIKI_FONT_STYLES = {"italic", "bold", "underline", "strikethrough"}


def palettes_dir() -> Path:
    return REPO_ROOT / "palettes"


def load_registry() -> dict[str, dict[str, Any]]:
    return registry_utils.load_registry(REPO_ROOT)


def resolve_path(repo_root: Path, value: str | None) -> Path | None:
    if value is None:
        return None
    return repo_root / value


def tool_manifest(registry: dict[str, dict[str, Any]], tool: str) -> dict[str, Any]:
    return registry_utils.get_tool(registry, tool)


def tool_template(manifest: dict[str, Any]) -> Path | None:
    return resolve_path(REPO_ROOT, manifest.get("template_path"))


def extra_templates(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    entries = manifest.get("extra_templates") or []
    resolved: list[dict[str, Any]] = []
    for entry in entries:
        template_path = resolve_path(REPO_ROOT, entry.get("template_path"))
        output_path = entry.get("output_path_template")
        if not template_path or not output_path:
            raise SystemExit("Error: extra_templates entries require template_path and output_path_template")
        resolved.append(
            {
                "template_path": template_path,
                "output_path_template": output_path,
                "notice_style": entry.get(
                    "notice_style", manifest.get("notice_style")
                ),
            }
        )
    return resolved


def extra_install_dirs(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    entries = manifest.get("extra_install_dirs") or []
    resolved: list[dict[str, Any]] = []
    for entry in entries:
        source_rel = entry.get("source_rel")
        dest_subdir = entry.get("dest_subdir", "")
        if not source_rel:
            raise SystemExit("Error: extra_install_dirs entries require source_rel")
        resolved.append(
            {
                "source_dir": resolve_path(REPO_ROOT, source_rel),
                "dest_subdir": dest_subdir,
            }
        )
    return resolved


def tool_out_dir(manifest: dict[str, Any], override: str | None) -> Path:
    if override:
        return Path(override)
    theme_dir = manifest.get("theme_dir_rel")
    if not theme_dir:
        raise SystemExit("Error: theme_dir_rel missing in manifest")
    return resolve_path(REPO_ROOT, theme_dir)


def tool_src_dir(manifest: dict[str, Any]) -> Path:
    theme_dir = manifest.get("theme_dir_rel")
    if not theme_dir:
        raise SystemExit("Error: theme_dir_rel missing in manifest")
    return resolve_path(REPO_ROOT, theme_dir)


def tool_package_dir(manifest: dict[str, Any]) -> Path:
    package_root = manifest.get("package_root_rel")
    if not package_root:
        raise SystemExit("Error: package_root_rel missing in package manifest")
    return resolve_path(REPO_ROOT, package_root)


def resolve_output_path(manifest: dict[str, Any], theme_name: str, out_dir_override: str | None) -> Path:
    theme_kind = manifest.get("theme_kind", "file")
    entry = manifest.get("theme_entry", "flavor.toml")
    template = manifest.get("output_path_template")
    theme_ext = manifest.get("theme_ext", "")

    if out_dir_override:
        base = Path(out_dir_override)
        if theme_kind == "dir":
            dir_suffix = manifest.get("dir_suffix", ".yazi")
            return base / f"{theme_name}{dir_suffix}" / entry
        suffix = theme_ext if theme_ext else ""
        return base / f"{theme_name}{suffix}"

    if template:
        return REPO_ROOT / template.replace("{theme}", theme_name)

    suffix = theme_ext if theme_ext else ""
    return tool_out_dir(manifest, None) / f"{theme_name}{suffix}"


def tool_default_themes_dir(manifest: dict[str, Any]) -> Path:
    install_targets = manifest.get("install_targets") or []
    for target in install_targets:
        if "$XDG_CONFIG_HOME" in target:
            return Path(target.replace("$XDG_CONFIG_HOME", str(paths.xdg_config_home())))
    if install_targets:
        return Path(os.path.expandvars(install_targets[0])).expanduser()
    raise SystemExit("Error: install_targets missing in manifest")


def tool_default_config_dir(manifest: dict[str, Any]) -> Path:
    config_locations = manifest.get("config_locations") or []
    for target in config_locations:
        if "$XDG_CONFIG_HOME" in target:
            return Path(target.replace("$XDG_CONFIG_HOME", str(paths.xdg_config_home())))
    if config_locations:
        return Path(os.path.expandvars(config_locations[0])).expanduser()
    raise SystemExit("Error: config_locations missing in manifest")


def theme_title(name: str) -> str:
    return " ".join([part.capitalize() for part in name.split("-")])


def swap_modus_variant(name: str) -> str:
    if "vivendi" in name:
        return name.replace("vivendi", "operandi", 1)
    if "operandi" in name:
        return name.replace("operandi", "vivendi", 1)
    return name


def json_path_exists(data: Any, path: str) -> bool:
    current = data
    for segment in path.split("."):
        if isinstance(current, list):
            if not segment.isdigit():
                return False
            index = int(segment)
            if index >= len(current):
                return False
            current = current[index]
            continue
        if not isinstance(current, dict):
            return False
        if segment not in current:
            return False
        current = current[segment]
    return current is not None


def validate_shiki_theme(data: Any, path: Path) -> list[str]:
    """Validate the strict source format used by the standalone Shiki port."""
    issues: list[str] = []
    if not isinstance(data, dict):
        return ["Theme document must be an object"]

    missing_keys = sorted(SHIKI_THEME_KEYS - set(data))
    unknown_keys = sorted(set(data) - SHIKI_THEME_KEYS)
    if missing_keys:
        issues.append(f"Missing top-level keys: {', '.join(missing_keys)}")
    if unknown_keys:
        issues.append(f"Unsupported top-level keys: {', '.join(unknown_keys)}")

    theme_name = data.get("name")
    if theme_name != path.stem:
        issues.append(f"name must match filename: {path.stem}")
    display_name = data.get("displayName")
    if not isinstance(display_name, str) or not display_name.strip():
        issues.append("displayName must be a non-empty string")

    expected_type = "light" if path.stem.startswith("modus-operandi") else "dark"
    if data.get("type") != expected_type:
        issues.append(f"type must be {expected_type}")

    for key in ("fg", "bg"):
        value = data.get(key)
        if not isinstance(value, str) or not HEX_COLOR_RE.fullmatch(value):
            issues.append(f"{key} must be a #RRGGBB color")

    colors = data.get("colors")
    if not isinstance(colors, dict):
        issues.append("colors must be an object")
    else:
        missing_colors = sorted(SHIKI_COLOR_KEYS - set(colors))
        unknown_colors = sorted(set(colors) - SHIKI_COLOR_KEYS)
        if missing_colors:
            issues.append(f"Missing colors: {', '.join(missing_colors)}")
        if unknown_colors:
            issues.append(f"Unsupported colors: {', '.join(unknown_colors)}")
        for key, value in colors.items():
            if not isinstance(value, str) or not HEX_COLOR_RE.fullmatch(value):
                issues.append(f"colors.{key} must be a #RRGGBB color")
        if data.get("fg") != colors.get("editor.foreground"):
            issues.append("fg must match colors.editor.foreground")
        if data.get("bg") != colors.get("editor.background"):
            issues.append("bg must match colors.editor.background")

    token_colors = data.get("tokenColors")
    if not isinstance(token_colors, list) or not token_colors:
        issues.append("tokenColors must be a non-empty array")
        return issues

    for index, rule in enumerate(token_colors):
        prefix = f"tokenColors.{index}"
        if not isinstance(rule, dict):
            issues.append(f"{prefix} must be an object")
            continue
        unknown_rule_keys = sorted(set(rule) - SHIKI_TOKEN_RULE_KEYS)
        if unknown_rule_keys:
            issues.append(
                f"{prefix} has unsupported keys: {', '.join(unknown_rule_keys)}"
            )
        if "name" in rule and (
            not isinstance(rule["name"], str) or not rule["name"].strip()
        ):
            issues.append(f"{prefix}.name must be a non-empty string")

        scopes = rule.get("scope")
        if not isinstance(scopes, list) or not scopes:
            issues.append(f"{prefix}.scope must be a non-empty array")
        else:
            for scope in scopes:
                if not isinstance(scope, str) or not scope.strip():
                    issues.append(f"{prefix}.scope entries must be non-empty strings")
                elif "," in scope:
                    issues.append(
                        f"{prefix}.scope entries must not pack comma-separated selectors"
                    )

        settings = rule.get("settings")
        if not isinstance(settings, dict) or not settings:
            issues.append(f"{prefix}.settings must be a non-empty object")
            continue
        unknown_setting_keys = sorted(set(settings) - SHIKI_TOKEN_SETTING_KEYS)
        if unknown_setting_keys:
            issues.append(
                f"{prefix}.settings has unsupported keys: "
                + ", ".join(unknown_setting_keys)
            )
        for key in ("foreground", "background"):
            if key not in settings:
                continue
            value = settings[key]
            if not isinstance(value, str) or not HEX_COLOR_RE.fullmatch(value):
                issues.append(f"{prefix}.settings.{key} must be a #RRGGBB color")
        if "fontStyle" in settings:
            font_style = settings["fontStyle"]
            if not isinstance(font_style, str):
                issues.append(f"{prefix}.settings.fontStyle must be a string")
            else:
                styles = font_style.split()
                unknown_styles = sorted(set(styles) - SHIKI_FONT_STYLES)
                if unknown_styles:
                    issues.append(
                        f"{prefix}.settings.fontStyle has unsupported values: "
                        + ", ".join(unknown_styles)
                    )
                if len(styles) != len(set(styles)):
                    issues.append(
                        f"{prefix}.settings.fontStyle must not repeat values"
                    )

    return issues


def require_installable(manifest: dict[str, Any], tool: str) -> None:
    if manifest.get("installable", True) is False:
        raise SystemExit(
            f"Error: {tool} is a source-only port and has no install or config target"
        )


def cmd_list(_args: argparse.Namespace) -> None:
    registry = load_registry()
    tools = sorted(registry.keys())
    print("Tools:")
    for tool in tools:
        print(f"- {tool}")

    for tool in tools:
        print("\n" + f"{tool.capitalize()} themes:")
        manifest = registry[tool]
        theme_kind = manifest.get("theme_kind", "file")
        theme_ext = manifest.get("theme_ext", "")
        dir_suffix = manifest.get("dir_suffix", ".yazi")
        themes = theme_ops.list_themes(tool_src_dir(manifest), theme_kind=theme_kind, theme_ext=theme_ext, dir_suffix=dir_suffix)
        if not themes:
            print("(none found)")
        else:
            for name in themes:
                print(f"- {name}")


def render_with_template(
    palette: dict[str, str],
    template_text: str,
    theme_name: str,
    notice_style: str,
) -> str:
    content = template_utils.render_template(template_text, palette, theme_name)
    return template_utils.add_notice(content, notice_style)


def cmd_render(args: argparse.Namespace) -> None:
    registry = load_registry()
    tools = sorted(registry.keys()) if args.tool == "all" else [args.tool]

    for tool in tools:
        manifest = tool_manifest(registry, tool)
        out_dir = tool_out_dir(manifest, args.out_dir)

        template_path = tool_template(manifest)
        if not template_path:
            raise SystemExit(f"Error: template_path missing for {tool}")

        template_text = template_path.read_text(encoding="utf-8")
        notice_style = manifest.get("notice_style")
        if notice_style not in template_utils.NOTICE_STYLES:
            raise SystemExit(f"Error: invalid notice_style for {tool}: {notice_style}")
        extra = extra_templates(manifest)
        extra_written = set()

        palette_files = sorted(palettes_dir().glob("*.json"))
        if not palette_files:
            raise SystemExit("Error: no palettes found. Run sync-upstream first.")

        out_dir.mkdir(parents=True, exist_ok=True)
        for palette_path in palette_files:
            theme_name, palette = io.load_palette(str(palette_path))
            if args.theme and theme_name != args.theme:
                continue
            content = render_with_template(
                palette, template_text, theme_name, notice_style
            )
            output_path = resolve_output_path(manifest, theme_name, args.out_dir)
            io.write_output(str(output_path), content)
            if not getattr(args, "quiet", False):
                print(f"Wrote {output_path}")
            for entry in extra:
                extra_text = entry["template_path"].read_text(encoding="utf-8")
                extra_content = render_with_template(
                    palette, extra_text, theme_name, entry["notice_style"]
                )
                if args.out_dir:
                    base_dir = output_path.parent
                    extra_path = base_dir / Path(entry["output_path_template"]).name
                else:
                    extra_path = REPO_ROOT / entry["output_path_template"].replace("{theme}", theme_name)
                if "{theme}" not in entry["output_path_template"]:
                    if str(extra_path) in extra_written:
                        continue
                    extra_written.add(str(extra_path))
                io.write_output(str(extra_path), extra_content)
                if not getattr(args, "quiet", False):
                    print(f"Wrote {extra_path}")


def cmd_validate(args: argparse.Namespace) -> None:
    registry = load_registry()
    tools = sorted(registry.keys()) if args.tool == "all" else [args.tool]

    for tool in tools:
        manifest = tool_manifest(registry, tool)
        themes_dir = tool_out_dir(manifest, args.themes_dir)
        required_keys = manifest.get("required_keys", [])
        validate_json = manifest.get("validate_json", False)
        required_fields = manifest.get("required_fields", [])
        theme_format = manifest.get("theme_format")

        # Template-based validation (key presence)
        errors = []
        theme_kind = manifest.get("theme_kind", "file")
        theme_entry = manifest.get("theme_entry", "flavor.toml")
        dir_suffix = manifest.get("dir_suffix", ".yazi")
        theme_ext = manifest.get("theme_ext", "")

        if theme_format == SHIKI_THEME_FORMAT and not args.theme:
            expected_files = {
                f"{path.stem}{theme_ext}" for path in palettes_dir().glob("*.json")
            }
            actual_files = {
                path.name
                for path in themes_dir.iterdir()
                if path.is_file() and not path.name.startswith(".")
            }
            missing_files = sorted(expected_files - actual_files)
            unexpected_files = sorted(actual_files - expected_files)
            directory_issues = []
            if missing_files:
                directory_issues.append(
                    f"Missing generated themes: {', '.join(missing_files)}"
                )
            if unexpected_files:
                directory_issues.append(
                    f"Unexpected generated themes: {', '.join(unexpected_files)}"
                )
            if directory_issues:
                errors.append((themes_dir, directory_issues))

        for path in sorted(themes_dir.iterdir()):
            if path.name.startswith("."):
                continue
            if theme_kind == "dir":
                if not path.is_dir():
                    continue
                if dir_suffix and not path.name.endswith(dir_suffix):
                    continue
                candidate = path / theme_entry
                if not candidate.is_file():
                    errors.append((path, [f"Missing {theme_entry}"]))
                    continue
                text = candidate.read_text(encoding="utf-8")
            else:
                if path.is_dir():
                    continue
                if args.theme and path.name != args.theme:
                    continue
                text = path.read_text(encoding="utf-8")
            if args.theme and theme_kind == "dir":
                if dir_suffix and not args.theme.endswith(dir_suffix):
                    expected = f"{args.theme}{dir_suffix}"
                else:
                    expected = args.theme
                if path.name != expected:
                    continue
            issues = []
            if validate_json:
                try:
                    data = json.loads(text)
                except json.JSONDecodeError as exc:
                    issues.append(f"Invalid JSON: {exc}")
                else:
                    for field in required_fields:
                        if not json_path_exists(data, field):
                            issues.append(f"Missing field: {field}")
                    if theme_format == SHIKI_THEME_FORMAT:
                        issues.extend(validate_shiki_theme(data, path))
            for key in required_keys:
                if key == "palette":
                    if "palette =" not in text:
                        issues.append("Missing palette entries")
                else:
                    if not re.search(
                        rf"^\s*{re.escape(key)}\s*(?:=|:)", text, re.MULTILINE
                    ):
                        issues.append(f"Missing key: {key}")
            if issues:
                errors.append((path, issues))

        for path, issues in errors:
            print(f"Invalid theme: {path}")
            for issue in issues:
                print(f"  {issue}")

        if errors:
            raise SystemExit(f"Validation failed for {len(errors)} theme(s).")

        if theme_kind == "dir":
            total = len(
                [
                    p
                    for p in themes_dir.iterdir()
                    if p.is_dir() and (not dir_suffix or p.name.endswith(dir_suffix))
                ]
            )
            if args.theme:
                if dir_suffix and not args.theme.endswith(dir_suffix):
                    name = f"{args.theme}{dir_suffix}"
                else:
                    name = args.theme
                total = 1 if (themes_dir / name).is_dir() else 0
        else:
            total = len([p for p in themes_dir.iterdir() if p.is_file() and not p.name.startswith('.')])
            if args.theme:
                total = 1 if (themes_dir / args.theme).is_file() else 0
        if not getattr(args, "quiet", False):
            print(f"Validated {total} theme(s).")


def cmd_install(args: argparse.Namespace) -> None:
    registry = load_registry()
    manifest = tool_manifest(registry, args.tool)
    require_installable(manifest, args.tool)
    dest_dir = Path(args.themes_dir) if args.themes_dir else tool_default_themes_dir(manifest)
    if args.copy and args.link:
        raise SystemExit("Error: choose either --copy or --link")
    mode = "copy" if args.copy else "link"
    if manifest.get("distribution", "loose") == "package":
        if args.theme:
            raise SystemExit(
                f"Error: {args.tool} is installed as a complete package; "
                "--theme is not supported"
            )
        theme_ops.install_package(tool_package_dir(manifest), dest_dir, mode)
        return

    src_dir = tool_src_dir(manifest)
    theme_kind = manifest.get("theme_kind", "file")
    theme_ext = manifest.get("theme_ext", "")
    dir_suffix = manifest.get("dir_suffix", ".yazi")
    theme_entry = manifest.get("theme_entry", "")
    symlink_entry_only = manifest.get("symlink_entry_only", False)
    theme_ops.install_themes(
        src_dir,
        dest_dir,
        mode,
        args.theme,
        theme_kind=theme_kind,
        theme_ext=theme_ext,
        dir_suffix=dir_suffix,
        theme_entry=theme_entry,
        symlink_entry_only=symlink_entry_only,
    )
    for entry in extra_install_dirs(manifest):
        extra_src = entry["source_dir"]
        extra_dest = dest_dir / entry["dest_subdir"]
        theme_ops.install_themes(extra_src, extra_dest, mode, None, theme_kind="file")


def cmd_uninstall(args: argparse.Namespace) -> None:
    registry = load_registry()
    manifest = tool_manifest(registry, args.tool)
    require_installable(manifest, args.tool)
    dest_dir = Path(args.themes_dir) if args.themes_dir else tool_default_themes_dir(manifest)
    if manifest.get("distribution", "loose") == "package":
        if args.theme:
            raise SystemExit(
                f"Error: {args.tool} is installed as a complete package; "
                "--theme is not supported"
            )
        theme_ops.uninstall_package(dest_dir, tool_package_dir(manifest))
        return

    src_dir = tool_src_dir(manifest)
    theme_kind = manifest.get("theme_kind", "file")
    theme_ext = manifest.get("theme_ext", "")
    dir_suffix = manifest.get("dir_suffix", ".yazi")
    theme_entry = manifest.get("theme_entry", "")
    symlink_entry_only = manifest.get("symlink_entry_only", False)
    theme_ops.uninstall_themes(
        dest_dir,
        src_dir,
        args.theme,
        theme_kind=theme_kind,
        theme_ext=theme_ext,
        dir_suffix=dir_suffix,
        theme_entry=theme_entry,
        symlink_entry_only=symlink_entry_only,
    )
    for entry in extra_install_dirs(manifest):
        extra_src = entry["source_dir"]
        extra_dest = dest_dir / entry["dest_subdir"]
        theme_ops.uninstall_themes(extra_dest, extra_src, None, theme_kind="file")


def cmd_print_config(args: argparse.Namespace) -> None:
    registry = load_registry()
    manifest = tool_manifest(registry, args.tool)
    require_installable(manifest, args.tool)
    if not args.theme:
        raise SystemExit("Error: --theme is required for print-config")

    config_dir = Path(args.config_dir) if args.config_dir else tool_default_config_dir(manifest)

    if args.tool == "ghostty":
        print(f"theme = {args.theme}")
        print(f"Config directory: {config_dir}")
        return

    if args.tool == "lazygit":
        src_dir = tool_src_dir(manifest)
        theme_ext = manifest.get("theme_ext", "")
        theme_file = theme_ops.find_theme_file(src_dir, args.theme, theme_ext)
        if theme_file is None:
            raise SystemExit(f"Error: theme not found: {args.theme}")
        print(f"# Paste into {config_dir}/config.yml")
        print(theme_file.read_text(encoding="utf-8"), end="")
        return

    if args.tool == "yazi":
        print("[flavor]")
        print(f"dark = \"{args.theme}\"")
        print(f"light = \"{args.theme}\"")
        print(f"# Config: {config_dir}")
        return

    if args.tool == "zed":
        if "vivendi" in args.theme:
            dark = theme_title(args.theme)
            light = theme_title(swap_modus_variant(args.theme))
        elif "operandi" in args.theme:
            light = theme_title(args.theme)
            dark = theme_title(swap_modus_variant(args.theme))
        else:
            light = theme_title(args.theme)
            dark = theme_title(args.theme)
        print("{")
        print("  \"theme\": {")
        print("    \"mode\": \"system\",")
        print(f"    \"light\": \"{light}\",")
        print(f"    \"dark\": \"{dark}\"")
        print("  }")
        print("}")
        print(f"# Config: {config_dir}")
        return

    if args.tool == "ls-colors":
        dest_dir = tool_default_themes_dir(manifest)
        if sys.platform == "darwin":
            print(f"# Add to {config_dir}")
            print(f"source \"{dest_dir}/bsd/modus-theme\"")
        else:
            print(f"# Add to {config_dir}")
            print(f"source \"{dest_dir}/{args.theme}\"")
        return

    if args.tool == "xcode":
        themes_dir = tool_default_themes_dir(manifest)
        print(f"# Themes directory: {themes_dir}")
        print("# Open Xcode -> Settings -> Themes and select:")
        print(args.theme)
        return

    if args.tool == "glamour":
        print("# Glamour is a shared style source.")
        print("# For Glow config, use:")
        print(f"python3 scripts/modus.py print-config --tool glow --theme {args.theme}")
        return

    if args.tool == "glow":
        src_dir = tool_src_dir(manifest)
        theme_ext = manifest.get("theme_ext", "")
        theme_file = theme_ops.find_theme_file(src_dir, args.theme, theme_ext)
        if theme_file is None:
            raise SystemExit(f"Error: theme not found: {args.theme}")
        themes_dir = tool_default_themes_dir(manifest)
        print(f"# Add to {config_dir}")
        print(f"style: \"{themes_dir / theme_file.name}\"")
        return


def emacs_bin() -> Path:
    if shutil.which("emacs"):
        return Path(shutil.which("emacs"))
    bundled = REPO_ROOT / ".emacs-app" / "Emacs.app" / "Contents" / "MacOS" / "Emacs"
    if bundled.exists():
        return bundled
    raise FileNotFoundError("Emacs not found. Run: python3 scripts/modus.py fetch-emacs")


def extract_palettes(source_dir: Path, out_dir: Path) -> None:
    emacs = emacs_bin()
    out_dir.mkdir(parents=True, exist_ok=True)
    elisp = REPO_ROOT / "scripts" / "core" / "extract-palettes.el"
    expr = f'(modus-themes-export-palettes "{source_dir}" "{out_dir}")'

    subprocess.run(
        [str(emacs), "-Q", "--batch", "-l", str(elisp), "--eval", expr],
        check=True,
    )


def cmd_fetch_emacs(_args: argparse.Namespace) -> None:
    if sys.platform != "darwin":
        raise SystemExit("Error: fetch-emacs is only supported on macOS.")

    emacs_dir = REPO_ROOT / ".emacs-app"
    emacs_app = emacs_dir / "Emacs.app"

    if emacs_app.is_dir():
        print(f"Emacs.app already present: {emacs_app}")
        return

    dmg_name = "Emacs-30.2-1-universal.dmg"
    dmg_url = "https://emacsformacosx.com/emacs-builds/Emacs-30.2-1-universal.dmg"
    dmg_path = emacs_dir / dmg_name

    emacs_dir.mkdir(parents=True, exist_ok=True)

    if not dmg_path.exists():
        print(f"Downloading {dmg_name}...")
        urllib.request.urlretrieve(dmg_url, dmg_path)
    else:
        print(f"DMG already present: {dmg_path}")

    result = subprocess.run(
        ["hdiutil", "attach", "-nobrowse", "-readonly", str(dmg_path)],
        check=True,
        capture_output=True,
        text=True,
    )

    mount_point = None
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    if lines:
        mount_point = lines[-1].split()[-1]

    if not mount_point:
        raise SystemExit("Error: failed to mount DMG.")

    try:
        source_app = Path(mount_point) / "Emacs.app"
        if not source_app.is_dir():
            raise SystemExit("Error: Emacs.app not found in DMG.")
        subprocess.run(["ditto", str(source_app), str(emacs_app)], check=True)
        print(f"Emacs.app installed to {emacs_app}")
    finally:
        subprocess.run(["hdiutil", "detach", mount_point, "-quiet"], check=False)


def load_upstream_lock() -> dict[str, str]:
    lock_path = REPO_ROOT / "upstream.lock.json"
    data = json.loads(lock_path.read_text(encoding="utf-8"))
    required = (
        "repository",
        "ref",
        "revision",
        "version",
        "palette_license",
        "palette_source",
    )
    if not isinstance(data, dict) or any(
        not isinstance(data.get(key), str) or not data[key] for key in required
    ):
        raise ValueError("upstream.lock.json is missing required string fields")
    return {key: data[key] for key in required}


def modus_version(source_dir: Path) -> str:
    source = source_dir / "modus-themes.el"
    match = re.search(
        r"^;; Version:\s+(\S+)", source.read_text(encoding="utf-8"), re.MULTILINE
    )
    if not match:
        raise ValueError("Could not determine Modus version")
    return match.group(1)


def update_notice_provenance(lock: dict[str, str]) -> None:
    notice_path = REPO_ROOT / "NOTICE"
    notice = notice_path.read_text(encoding="utf-8")
    replacement = (
        f"The current palette snapshot was extracted from Modus Themes "
        f"{lock['version']} at upstream commit\n{lock['revision']}"
    )
    updated, replacements = re.subn(
        r"The current palette snapshot was extracted from Modus Themes \S+ "
        r"at upstream commit\n"
        r"[0-9a-f]{40}",
        replacement,
        notice,
    )
    if replacements != 1:
        raise ValueError("Could not update palette provenance in NOTICE")
    if updated != notice:
        notice_path.write_text(updated, encoding="utf-8")
        print(f"Updated {notice_path}")


def cmd_sync_upstream(args: argparse.Namespace) -> None:
    try:
        lock = load_upstream_lock()
        emacs_bin()
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as exc:
        raise SystemExit(f"Error: {exc}") from exc

    target = args.revision or lock["ref"]
    with tempfile.TemporaryDirectory(prefix="modus-themes-") as temp_dir:
        source_dir = Path(temp_dir) / "source"
        extracted_dir = Path(temp_dir) / "palettes"
        subprocess.run(["git", "init", "--quiet", str(source_dir)], check=True)
        subprocess.run(
            ["git", "-C", str(source_dir), "remote", "add", "origin", lock["repository"]],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(source_dir), "fetch", "--quiet", "--depth=1", "origin", target],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(source_dir), "checkout", "--quiet", "--detach", "FETCH_HEAD"],
            check=True,
        )
        revision = subprocess.run(
            ["git", "-C", str(source_dir), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        extract_palettes(source_dir, extracted_dir)

        generated = sorted(extracted_dir.glob("*.json"))
        if not generated:
            raise SystemExit("Error: upstream extraction produced no palettes")
        for existing in palettes_dir().glob("*.json"):
            existing.unlink()
        for palette_path in generated:
            shutil.copy2(palette_path, palettes_dir() / palette_path.name)

        lock.update(revision=revision, version=modus_version(source_dir))

    lock_path = REPO_ROOT / "upstream.lock.json"
    lock_path.write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")
    update_notice_provenance(lock)
    cmd_render(argparse.Namespace(tool="all", out_dir=None, theme=None))


def report_issues(label: str, issues: list[str]) -> None:
    if not issues:
        return
    print(f"{label} found issues:")
    for issue in issues:
        print(f"- {issue}")
    raise SystemExit(f"{label} failed.")


def cmd_doctor(_args: argparse.Namespace) -> None:
    issues = []
    for command in ("git", "python3"):
        if shutil.which(command) is None:
            issues.append(f"{command} not found")
    if shutil.which("trash") is None:
        issues.append("trash not found (needed for uninstall)")
    try:
        emacs_bin()
    except FileNotFoundError as exc:
        issues.append(str(exc))

    report_issues("Doctor", issues)
    print("Doctor passed.")


def check_source() -> None:
    issues: list[str] = []

    required_files = (
        REPO_ROOT / "LICENSE",
        REPO_ROOT / "NOTICE",
        REPO_ROOT / "LICENSES" / "MIT.txt",
        REPO_ROOT / "LICENSES" / "CC0-1.0.txt",
        REPO_ROOT / "ports" / "NOTICE",
        REPO_ROOT / "ports" / "vscode" / "extension-root" / "LICENSE",
        REPO_ROOT / "ports" / "vscode" / "extension-root" / "NOTICE",
        REPO_ROOT / "upstream.lock.json",
    )
    for required_file in required_files:
        if not required_file.is_file():
            issues.append(f"required file missing: {required_file.relative_to(REPO_ROOT)}")

    notice_path = REPO_ROOT / "NOTICE"
    if notice_path.is_file():
        try:
            notice_text = notice_path.read_text(encoding="utf-8")
            lock = load_upstream_lock()
            expected = (
                f"Modus Themes {lock['version']} at upstream commit\n"
                f"{lock['revision']}"
            )
            if expected not in notice_text:
                issues.append(
                    "NOTICE palette provenance is stale "
                    f"(expected {lock['version']} at {lock['revision']})"
                )
            if lock["palette_license"] != "CC0-1.0":
                issues.append("upstream lock must declare CC0-1.0 palette data")
            if lock["palette_source"] != PALETTE_SOURCE:
                issues.append("upstream lock has the wrong palette source")
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            issues.append(f"could not validate palette provenance: {exc}")

    ports_notice = REPO_ROOT / "ports" / "NOTICE"
    if ports_notice.is_file():
        ports_notice_text = ports_notice.read_text(encoding="utf-8")
        for marker in ("MIT", "CC0-1.0", PALETTE_SOURCE):
            if marker not in ports_notice_text:
                issues.append(f"ports/NOTICE missing marker: {marker}")

    vscode_license = REPO_ROOT / "ports" / "vscode" / "extension-root" / "LICENSE"
    mit_license = REPO_ROOT / "LICENSES" / "MIT.txt"
    if vscode_license.is_file() and mit_license.is_file():
        if vscode_license.read_bytes() != mit_license.read_bytes():
            issues.append("VS Code extension LICENSE differs from LICENSES/MIT.txt")

    vscode_notice = REPO_ROOT / "ports" / "vscode" / "extension-root" / "NOTICE"
    if vscode_notice.is_file():
        vscode_notice_text = vscode_notice.read_text(encoding="utf-8")
        for marker in ("MIT", "CC0-1.0", PALETTE_SOURCE):
            if marker not in vscode_notice_text:
                issues.append(f"VS Code extension NOTICE missing marker: {marker}")

    vscode_package = REPO_ROOT / "ports" / "vscode" / "extension-root" / "package.json"
    if vscode_package.is_file():
        try:
            package = json.loads(vscode_package.read_text(encoding="utf-8"))
            if not isinstance(package, dict) or package.get("license") != "MIT":
                issues.append("VS Code extension package must declare the MIT license")
            contributes = package.get("contributes") if isinstance(package, dict) else None
            themes = contributes.get("themes") if isinstance(contributes, dict) else None
            if not isinstance(themes, list):
                issues.append("VS Code extension package must contribute themes")
            else:
                for theme in themes:
                    relative_path = theme.get("path") if isinstance(theme, dict) else None
                    if not isinstance(relative_path, str):
                        issues.append("VS Code extension has an invalid theme path")
                        continue
                    theme_path = vscode_package.parent / relative_path
                    if not theme_path.is_file():
                        issues.append(
                            f"VS Code extension theme missing: {relative_path}"
                        )
        except json.JSONDecodeError as exc:
            issues.append(f"VS Code extension package invalid: {exc}")

    extractor_path = REPO_ROOT / "scripts" / "core" / "extract-palettes.el"
    if extractor_path.is_file():
        extractor_text = extractor_path.read_text(encoding="utf-8")
        if not re.search(
            r"\(modus-themes-common-palette-overrides\s+nil\)", extractor_text
        ):
            issues.append("palette extractor must explicitly disable upstream overrides")
        if "modus-themes-preset-overrides-" in extractor_text:
            issues.append("palette extractor must not import an upstream preset")
        if not re.search(
            r"\(modus-themes-get-theme-palette\s+"
            r"\(intern theme-name\)\s+nil\s+nil\)",
            extractor_text,
        ):
            issues.append("palette extractor must request core palette data only")
    else:
        issues.append("palette extractor missing: scripts/core/extract-palettes.el")

    palette_files = sorted(palettes_dir().glob("*.json"))
    loaded_palettes: list[tuple[str, dict[str, str]]] = []
    if not palette_files:
        issues.append("no palettes found (run: python3 scripts/modus.py sync-upstream)")
    for palette_path in palette_files:
        try:
            data = json.loads(palette_path.read_text(encoding="utf-8"))
            theme_name, palette = io.load_palette(str(palette_path))
            if data["license"] != "CC0-1.0":
                issues.append(f"{palette_path.name}: missing CC0-1.0 metadata")
            if data["source"] != PALETTE_SOURCE:
                issues.append(f"{palette_path.name}: missing palette source metadata")
            if theme_name != palette_path.stem:
                issues.append(
                    f"{palette_path.name}: name does not match filename: {theme_name}"
                )
            loaded_palettes.append((theme_name, palette))
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            issues.append(f"{palette_path.name}: {exc}")

    palette_keys: set[str] = set()
    if loaded_palettes:
        key_sets = [set(palette) for _, palette in loaded_palettes]
        palette_keys = set.intersection(*key_sets)
        if any(keys != key_sets[0] for keys in key_sets[1:]):
            issues.append("palette key sets differ between themes")

    try:
        registry = load_registry()
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        issues.append(f"tool registry invalid: {exc}")
        registry = {}

    templates: dict[Path, set[str]] = {}
    for tool, manifest in registry.items():
        for field in ("theme_dir_rel", "template_path", "notice_style"):
            if not manifest.get(field):
                issues.append(f"{tool}: missing manifest field: {field}")
        installable = manifest.get("installable", True)
        if not isinstance(installable, bool):
            issues.append(f"{tool}: installable must be a boolean")
        elif not installable:
            if manifest.get("install_targets"):
                issues.append(
                    f"{tool}: source-only ports must not declare install_targets"
                )
            if manifest.get("config_locations"):
                issues.append(
                    f"{tool}: source-only ports must not declare config_locations"
                )
        theme_format = manifest.get("theme_format")
        if theme_format not in (None, SHIKI_THEME_FORMAT):
            issues.append(f"{tool}: unsupported theme_format: {theme_format}")
        if theme_format == SHIKI_THEME_FORMAT and not manifest.get("validate_json"):
            issues.append(f"{tool}: {SHIKI_THEME_FORMAT} requires validate_json")
        distribution = manifest.get("distribution", "loose")
        if distribution not in ("loose", "package"):
            issues.append(f"{tool}: invalid distribution: {distribution}")
        if distribution == "package":
            package_root = resolve_path(REPO_ROOT, manifest.get("package_root_rel"))
            if package_root is None or not package_root.is_dir():
                issues.append(
                    f"{tool}: package root missing: {manifest.get('package_root_rel')}"
                )
            else:
                theme_dir = resolve_path(REPO_ROOT, manifest.get("theme_dir_rel"))
                try:
                    if theme_dir is None:
                        raise ValueError
                    theme_dir.relative_to(package_root)
                except ValueError:
                    issues.append(f"{tool}: theme_dir_rel must be inside package_root_rel")
        notice_style = manifest.get("notice_style")
        if notice_style not in template_utils.NOTICE_STYLES:
            issues.append(f"{tool}: invalid notice_style: {notice_style}")

        template_path = tool_template(manifest)
        if template_path is None or not template_path.is_file():
            issues.append(f"{tool}: template missing: {manifest.get('template_path')}")
        else:
            templates.setdefault(template_path, set()).add(tool)

        for entry in manifest.get("extra_templates") or []:
            extra_template = resolve_path(REPO_ROOT, entry.get("template_path"))
            output_template = entry.get("output_path_template")
            extra_style = entry.get("notice_style", notice_style)
            if extra_template is None or not extra_template.is_file():
                issues.append(
                    f"{tool}: extra template missing: {entry.get('template_path')}"
                )
            else:
                templates.setdefault(extra_template, set()).add(tool)
            if not output_template:
                issues.append(f"{tool}: extra template missing output_path_template")
            if extra_style not in template_utils.NOTICE_STYLES:
                issues.append(f"{tool}: invalid extra notice_style: {extra_style}")

    for template_path, tools in sorted(templates.items()):
        template_text = template_path.read_text(encoding="utf-8")
        owner = ", ".join(sorted(tools))
        for error in template_utils.validate_template(template_text, palette_keys):
            issues.append(f"{owner}: {error}")
        for marker in template_utils.NOTICE_MARKERS:
            if marker in template_text:
                issues.append(
                    f"{template_path.relative_to(REPO_ROOT)}: generated notice is hard-coded"
                )
                break

    contrast_warnings = []
    for theme_name, palette in loaded_palettes:
        for warning in contrast_utils.validate_palette_contrast(palette):
            contrast_warnings.append(f"{theme_name}: {warning}")
    if contrast_warnings:
        print("Contrast warnings (may be intentional for tinted variants):")
        for warning in contrast_warnings:
            print(f"  - {warning}")

    report_issues("Source check", issues)


def check_generated() -> None:
    issues: list[str] = []
    try:
        registry = load_registry()
        theme_names = [
            io.load_palette(str(path))[0]
            for path in sorted(palettes_dir().glob("*.json"))
        ]
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        report_issues("Generated check", [str(exc)])
        return

    checked_paths: set[Path] = set()
    with tempfile.TemporaryDirectory(prefix="modus-render-check-") as temp_dir:
        for tool, manifest in registry.items():
            tool_dir = Path(temp_dir) / tool
            try:
                cmd_render(
                    argparse.Namespace(
                        tool=tool,
                        out_dir=str(tool_dir),
                        theme=None,
                        quiet=True,
                    )
                )
                cmd_validate(
                    argparse.Namespace(
                        tool=tool,
                        themes_dir=str(tool_dir),
                        theme=None,
                        quiet=True,
                    )
                )
                extras = extra_templates(manifest)
            except (OSError, KeyError, TypeError, ValueError, SystemExit) as exc:
                issues.append(f"{tool}: render or validation failed: {exc}")
                continue

            rendered_paths: dict[Path, tuple[Path, str]] = {}
            for theme_name in theme_names:
                rendered = resolve_output_path(manifest, theme_name, str(tool_dir))
                tracked = resolve_output_path(manifest, theme_name, None)
                rendered_paths[rendered] = (tracked, manifest["notice_style"])
                for entry in extras:
                    extra_rendered = rendered.parent / Path(
                        entry["output_path_template"]
                    ).name
                    extra_tracked = REPO_ROOT / entry[
                        "output_path_template"
                    ].replace("{theme}", theme_name)
                    rendered_paths[extra_rendered] = (
                        extra_tracked,
                        entry["notice_style"],
                    )

            for rendered, (tracked, notice_style) in rendered_paths.items():
                checked_paths.add(tracked)
                relative = tracked.relative_to(REPO_ROOT)
                if not rendered.is_file():
                    issues.append(f"{tool}: rendered output missing: {rendered}")
                    continue
                if not tracked.is_file():
                    issues.append(f"tracked generated output missing: {relative}")
                    continue
                if rendered.read_bytes() != tracked.read_bytes():
                    issues.append(f"tracked generated output is stale: {relative}")
                if notice_style != "sidecar":
                    output_text = rendered.read_text(encoding="utf-8")
                    for marker in template_utils.NOTICE_MARKERS:
                        if marker not in output_text:
                            issues.append(f"{relative}: missing generated notice: {marker}")

    report_issues("Generated check", issues)
    print(f"Checked {len(checked_paths)} generated outputs.")


def cmd_check(args: argparse.Namespace) -> None:
    if args.scope in (None, "source"):
        check_source()
        print("Source check passed.")
    if args.scope in (None, "generated"):
        check_generated()
        print("Generated check passed.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list").set_defaults(func=cmd_list)

    render_cmd = sub.add_parser("render")
    render_cmd.add_argument("--tool", required=True)
    render_cmd.add_argument("--out-dir")
    render_cmd.add_argument("--theme")
    render_cmd.set_defaults(func=cmd_render)

    validate_cmd = sub.add_parser("validate")
    validate_cmd.add_argument("--tool", required=True)
    validate_cmd.add_argument("--themes-dir")
    validate_cmd.add_argument("--theme")
    validate_cmd.set_defaults(func=cmd_validate)

    install_cmd = sub.add_parser("install")
    install_cmd.add_argument("--tool", required=True)
    install_cmd.add_argument("--theme")
    install_cmd.add_argument("--themes-dir")
    install_cmd.add_argument("--config-dir")
    install_cmd.add_argument("--link", action="store_true")
    install_cmd.add_argument("--copy", action="store_true")
    install_cmd.set_defaults(func=cmd_install)

    uninstall_cmd = sub.add_parser("uninstall")
    uninstall_cmd.add_argument("--tool", required=True)
    uninstall_cmd.add_argument("--theme")
    uninstall_cmd.add_argument("--themes-dir")
    uninstall_cmd.set_defaults(func=cmd_uninstall)

    print_cmd = sub.add_parser("print-config")
    print_cmd.add_argument("--tool", required=True)
    print_cmd.add_argument("--theme")
    print_cmd.add_argument("--config-dir")
    print_cmd.set_defaults(func=cmd_print_config)

    sub.add_parser("fetch-emacs").set_defaults(func=cmd_fetch_emacs)
    sync_cmd = sub.add_parser("sync-upstream")
    sync_cmd.add_argument("--revision")
    sync_cmd.set_defaults(func=cmd_sync_upstream)
    sub.add_parser("doctor").set_defaults(func=cmd_doctor)
    check_cmd = sub.add_parser("check")
    check_cmd.add_argument("scope", nargs="?", choices=("source", "generated"))
    check_cmd.set_defaults(func=cmd_check)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
