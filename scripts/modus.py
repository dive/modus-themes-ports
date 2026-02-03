#!/usr/bin/env python3
import argparse
import os
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
from scripts.common import paths
from scripts.common import render
from scripts.common import theme_ops
from scripts.common import validate

TOOLS = ["ghostty", "lazygit"]


def require_tool(tool: str):
    if tool not in TOOLS:
        raise ValueError(f"Unknown tool: {tool}")


def palettes_dir() -> Path:
    return REPO_ROOT / "palettes"


def tool_spec(tool: str) -> Path:
    return paths.spec_path(tool, REPO_ROOT)


def tool_mapping(tool: str, override: Optional[str]) -> Path:
    return Path(override) if override else paths.default_mapping(tool, REPO_ROOT)


def tool_out_dir(tool: str, override: Optional[str]) -> Path:
    return Path(override) if override else paths.default_output_dir(tool, REPO_ROOT)


def tool_src_dir(tool: str) -> Path:
    return REPO_ROOT / "ports" / tool / "themes"


def tool_default_themes_dir(tool: str) -> Path:
    if tool == "ghostty":
        return paths.ghostty_themes_dir()
    if tool == "lazygit":
        return paths.lazygit_themes_dir()
    raise ValueError(f"Unknown tool: {tool}")


def tool_default_config_dir(tool: str) -> Path:
    if tool == "ghostty":
        return paths.ghostty_config_dir()
    if tool == "lazygit":
        return paths.lazygit_config_dir()
    raise ValueError(f"Unknown tool: {tool}")


def cmd_list(_args):
    print("Tools:")
    for tool in TOOLS:
        print(f"- {tool}")

    for tool in TOOLS:
        print("\n" + f"{tool.capitalize()} themes:")
        themes = theme_ops.list_themes(tool_src_dir(tool))
        if not themes:
            print("(none found)")
        else:
            for name in themes:
                print(f"- {name}")


def cmd_render(args):
    require_tool(args.tool)
    outputs = render.render_all(
        palettes_dir(),
        tool_mapping(args.tool, args.mapping),
        tool_out_dir(args.tool, args.out_dir),
        tool_spec(args.tool),
    )
    for output in outputs:
        print(f"Wrote {output}")


def cmd_validate(args):
    require_tool(args.tool)
    validated, errors = validate.validate_all(
        tool_out_dir(args.tool, args.themes_dir),
        tool_spec(args.tool),
    )

    for path, issues in errors:
        print(f"Invalid theme: {path}")
        for issue in issues:
            print(f"  {issue}")

    if errors:
        raise SystemExit(f"Validation failed for {len(errors)} theme(s).")

    print(f"Validated {validated} theme(s).")


def cmd_install(args):
    require_tool(args.tool)
    src_dir = tool_src_dir(args.tool)
    dest_dir = Path(args.themes_dir) if args.themes_dir else tool_default_themes_dir(args.tool)
    if args.copy and args.link:
        raise SystemExit("Error: choose either --copy or --link")
    mode = "copy" if args.copy else "link"
    theme_ops.install_themes(src_dir, dest_dir, mode, args.theme)


def cmd_uninstall(args):
    require_tool(args.tool)
    src_dir = tool_src_dir(args.tool)
    dest_dir = Path(args.themes_dir) if args.themes_dir else tool_default_themes_dir(args.tool)
    theme_ops.uninstall_themes(dest_dir, src_dir, args.theme)


def cmd_print_config(args):
    require_tool(args.tool)
    if not args.theme:
        raise SystemExit("Error: --theme is required for print-config")

    config_dir = Path(args.config_dir) if args.config_dir else tool_default_config_dir(args.tool)

    if args.tool == "ghostty":
        print(f"theme = {args.theme}")
        print(f"Config directory: {config_dir}")
        return

    if args.tool == "lazygit":
        src_dir = tool_src_dir(args.tool)
        theme_file = theme_ops.find_theme_file(src_dir, args.theme)
        if theme_file is None:
            raise SystemExit(f"Error: theme not found: {args.theme}")
        print(f"# Paste into {config_dir}/config.yml")
        print(theme_file.read_text(encoding="utf-8"), end="")
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
    cmd_render(argparse.Namespace(tool="ghostty", mapping=None, out_dir=None))
    cmd_render(argparse.Namespace(tool="lazygit", mapping=None, out_dir=None))


def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list").set_defaults(func=cmd_list)

    render_cmd = sub.add_parser("render")
    render_cmd.add_argument("--tool", required=True)
    render_cmd.add_argument("--mapping")
    render_cmd.add_argument("--out-dir")
    render_cmd.set_defaults(func=cmd_render)

    validate_cmd = sub.add_parser("validate")
    validate_cmd.add_argument("--tool", required=True)
    validate_cmd.add_argument("--themes-dir")
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

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
