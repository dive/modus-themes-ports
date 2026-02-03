#!/usr/bin/env python3
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.common import git as git_utils
from scripts.common import io
from scripts.common import paths
from scripts.common import registry as registry_utils
from scripts.common import render
from scripts.common import template as template_utils
from scripts.common import theme_ops
from scripts.common import validate


def palettes_dir() -> Path:
    return REPO_ROOT / "palettes"


def load_registry():
    return registry_utils.load_registry(REPO_ROOT)


def resolve_path(repo_root: Path, value: Optional[str]) -> Optional[Path]:
    if value is None:
        return None
    return repo_root / value


def tool_manifest(registry: dict, tool: str) -> dict:
    return registry_utils.get_tool(registry, tool)


def tool_spec(manifest: dict) -> Optional[Path]:
    return resolve_path(REPO_ROOT, manifest.get("spec_path"))


def tool_mapping(manifest: dict, override: Optional[str]) -> Path:
    if override:
        return Path(override)
    mapping_path = manifest.get("mapping_path")
    if not mapping_path:
        raise SystemExit("Error: mapping_path missing in manifest")
    return resolve_path(REPO_ROOT, mapping_path)


def tool_template(manifest: dict) -> Optional[Path]:
    return resolve_path(REPO_ROOT, manifest.get("template_path"))


def extra_templates(manifest: dict):
    entries = manifest.get("extra_templates") or []
    resolved = []
    for entry in entries:
        template_path = resolve_path(REPO_ROOT, entry.get("template_path"))
        output_path = entry.get("output_path_template")
        if not template_path or not output_path:
            raise SystemExit("Error: extra_templates entries require template_path and output_path_template")
        resolved.append(
            {
                "template_path": template_path,
                "output_path_template": output_path,
            }
        )
    return resolved


def extra_install_dirs(manifest: dict):
    entries = manifest.get("extra_install_dirs") or []
    resolved = []
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


def tool_out_dir(manifest: dict, override: Optional[str]) -> Path:
    if override:
        return Path(override)
    theme_dir = manifest.get("theme_dir_rel")
    if not theme_dir:
        raise SystemExit("Error: theme_dir_rel missing in manifest")
    return resolve_path(REPO_ROOT, theme_dir)


def tool_src_dir(manifest: dict) -> Path:
    theme_dir = manifest.get("theme_dir_rel")
    if not theme_dir:
        raise SystemExit("Error: theme_dir_rel missing in manifest")
    return resolve_path(REPO_ROOT, theme_dir)


def resolve_output_path(manifest: dict, theme_name: str, out_dir_override: Optional[str]) -> Path:
    theme_kind = manifest.get("theme_kind", "file")
    entry = manifest.get("theme_entry", "flavor.toml")
    template = manifest.get("output_path_template")
    theme_ext = manifest.get("theme_ext", "")

    if out_dir_override:
        base = Path(out_dir_override)
        if theme_kind == "dir":
            return base / f"{theme_name}.yazi" / entry
        suffix = theme_ext if theme_ext else ""
        return base / f"{theme_name}{suffix}"

    if template:
        return REPO_ROOT / template.replace("{theme}", theme_name)

    suffix = theme_ext if theme_ext else ""
    return tool_out_dir(manifest, None) / f"{theme_name}{suffix}"


def tool_default_themes_dir(manifest: dict) -> Path:
    install_targets = manifest.get("install_targets") or []
    for target in install_targets:
        if "$XDG_CONFIG_HOME" in target:
            return Path(target.replace("$XDG_CONFIG_HOME", str(paths.xdg_config_home())))
    if install_targets:
        return Path(os.path.expandvars(install_targets[0])).expanduser()
    raise SystemExit("Error: install_targets missing in manifest")


def tool_default_config_dir(manifest: dict) -> Path:
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


def json_path_exists(data, path: str) -> bool:
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


def cmd_list(_args):
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


def render_with_template(manifest: dict, palette: dict, mapping: dict, template_text: str, theme_name: str) -> str:
    return template_utils.render_template(template_text, palette, mapping, theme_name)


def cmd_render(args):
    registry = load_registry()
    tools = sorted(registry.keys()) if args.tool == "all" else [args.tool]

    for tool in tools:
        manifest = tool_manifest(registry, tool)
        spec = tool_spec(manifest)
        mapping = tool_mapping(manifest, args.mapping)
        out_dir = tool_out_dir(manifest, args.out_dir)

        if spec:
            outputs = render.render_all(
                palettes_dir(),
                mapping,
                out_dir,
                spec,
                theme=args.theme,
            )
            for output in outputs:
                print(f"Wrote {output}")
            continue

        template_path = tool_template(manifest)
        if not template_path:
            raise SystemExit(f"Error: no spec_path or template_path for {tool}")

        template_text = template_path.read_text(encoding="utf-8")
        mapping_data = io.load_mapping(str(mapping))
        extra = extra_templates(manifest)
        extra_written = set()

        palette_files = sorted(palettes_dir().glob("*.json"))
        if not palette_files:
            raise SystemExit("Error: no palettes found. Run extract-palettes first.")

        out_dir.mkdir(parents=True, exist_ok=True)
        for palette_path in palette_files:
            theme_name, palette = io.load_palette(str(palette_path))
            if args.theme and theme_name != args.theme:
                continue
            content = render_with_template(manifest, palette, mapping_data, template_text, theme_name)
            output_path = resolve_output_path(manifest, theme_name, args.out_dir)
            io.write_output(str(output_path), content)
            print(f"Wrote {output_path}")
            for entry in extra:
                extra_text = entry["template_path"].read_text(encoding="utf-8")
                extra_content = render_with_template(manifest, palette, mapping_data, extra_text, theme_name)
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
                print(f"Wrote {extra_path}")


def cmd_validate(args):
    registry = load_registry()
    tools = sorted(registry.keys()) if args.tool == "all" else [args.tool]

    for tool in tools:
        manifest = tool_manifest(registry, tool)
        spec = tool_spec(manifest)
        themes_dir = tool_out_dir(manifest, args.themes_dir)
        required_keys = manifest.get("required_keys", [])
        validate_json = manifest.get("validate_json", False)
        required_fields = manifest.get("required_fields", [])

        if spec:
            validated, errors = validate.validate_all(themes_dir, spec, theme=args.theme)
            for path, issues in errors:
                print(f"Invalid theme: {path}")
                for issue in issues:
                    print(f"  {issue}")
            if errors:
                raise SystemExit(f"Validation failed for {len(errors)} theme(s).")
            print(f"Validated {validated} theme(s).")
            continue

        # Template-based validation (key presence)
        errors = []
        theme_kind = manifest.get("theme_kind", "file")
        theme_entry = manifest.get("theme_entry", "flavor.toml")

        for path in sorted(themes_dir.iterdir()):
            if path.name.startswith("."):
                continue
            if theme_kind == "dir":
                if not path.is_dir():
                    continue
                if not path.name.endswith(".yazi"):
                    continue
                candidate = path / theme_entry
                if not candidate.is_file():
                    errors.append((path, ["Missing flavor.toml"]))
                    continue
                text = candidate.read_text(encoding="utf-8")
            else:
                if path.is_dir():
                    continue
                if args.theme and path.name != args.theme:
                    continue
                text = path.read_text(encoding="utf-8")
            if args.theme and theme_kind == "dir":
                expected = args.theme if args.theme.endswith(".yazi") else f"{args.theme}.yazi"
                if path.name != expected:
                    continue
            if tool == "lazygit":
                issues = validate_lazygit.validate(text, required_keys)
            else:
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
                for key in required_keys:
                    if key == "palette":
                        if "palette =" not in text:
                            issues.append("Missing palette entries")
                    else:
                        if not re.search(rf"^\s*{re.escape(key)}\s*=", text, re.MULTILINE):
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
            total = len([p for p in themes_dir.iterdir() if p.is_dir() and p.name.endswith(".yazi")])
            if args.theme:
                name = args.theme if args.theme.endswith(".yazi") else f"{args.theme}.yazi"
                total = 1 if (themes_dir / name).is_dir() else 0
        else:
            total = len([p for p in themes_dir.iterdir() if p.is_file() and not p.name.startswith('.')])
            if args.theme:
                total = 1 if (themes_dir / args.theme).is_file() else 0
        print(f"Validated {total} theme(s).")


def cmd_install(args):
    registry = load_registry()
    manifest = tool_manifest(registry, args.tool)
    src_dir = tool_src_dir(manifest)
    dest_dir = Path(args.themes_dir) if args.themes_dir else tool_default_themes_dir(manifest)
    if args.copy and args.link:
        raise SystemExit("Error: choose either --copy or --link")
    mode = "copy" if args.copy else "link"
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


def cmd_uninstall(args):
    registry = load_registry()
    manifest = tool_manifest(registry, args.tool)
    src_dir = tool_src_dir(manifest)
    dest_dir = Path(args.themes_dir) if args.themes_dir else tool_default_themes_dir(manifest)
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


def cmd_print_config(args):
    registry = load_registry()
    manifest = tool_manifest(registry, args.tool)
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


def emacs_bin() -> Path:
    if shutil.which("emacs"):
        return Path(shutil.which("emacs"))
    bundled = REPO_ROOT / ".emacs-app" / "Emacs.app" / "Contents" / "MacOS" / "Emacs"
    if bundled.exists():
        return bundled
    raise FileNotFoundError("Emacs not found. Run: python3 scripts/modus.py fetch-emacs")


def cmd_extract_palettes(_args):
    vendor_dir = REPO_ROOT / "vendor" / "modus-themes"
    out_dir = REPO_ROOT / "palettes"
    if not vendor_dir.is_dir():
        raise SystemExit(f"Error: missing subtree at {vendor_dir}")

    try:
        emacs = emacs_bin()
    except FileNotFoundError as exc:
        raise SystemExit(f"Error: {exc}") from exc
    out_dir.mkdir(parents=True, exist_ok=True)
    elisp = REPO_ROOT / "scripts" / "core" / "extract-palettes.el"
    expr = f'(modus-themes-export-palettes "{vendor_dir}" "{out_dir}")'

    subprocess.run(
        [str(emacs), "-Q", "--batch", "-l", str(elisp), "--eval", expr],
        check=True,
    )


def cmd_fetch_emacs(_args):
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


def cmd_update_subtree(_args):
    remote_url = "https://github.com/protesilaos/modus-themes"
    prefix = "vendor/modus-themes"
    git_utils.subtree_update(str(REPO_ROOT), remote_url, prefix)
    cmd_extract_palettes(None)
    cmd_render(argparse.Namespace(tool="all", mapping=None, out_dir=None))


def cmd_doctor(_args):
    issues = []

    if shutil.which("git") is None:
        issues.append("git not found")
    if shutil.which("python3") is None:
        issues.append("python3 not found")
    if shutil.which("trash") is None:
        issues.append("trash not found (needed for uninstall)")

    try:
        emacs_bin()
    except FileNotFoundError:
        issues.append("emacs not found (run: python3 scripts/modus.py fetch-emacs)")

    if not (REPO_ROOT / "palettes").is_dir():
        issues.append("palettes directory missing (run: python3 scripts/modus.py extract-palettes)")

    if issues:
        print("Doctor found issues:")
        for issue in issues:
            print(f"- {issue}")
        raise SystemExit("Doctor failed.")

    print("Doctor passed.")


def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list").set_defaults(func=cmd_list)

    render_cmd = sub.add_parser("render")
    render_cmd.add_argument("--tool", required=True)
    render_cmd.add_argument("--mapping")
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

    sub.add_parser("extract-palettes").set_defaults(func=cmd_extract_palettes)
    sub.add_parser("fetch-emacs").set_defaults(func=cmd_fetch_emacs)
    sub.add_parser("update-subtree").set_defaults(func=cmd_update_subtree)
    sub.add_parser("doctor").set_defaults(func=cmd_doctor)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
