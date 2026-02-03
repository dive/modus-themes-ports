#!/usr/bin/env python3
import os
import shutil
import subprocess
from pathlib import Path


def list_themes(dir_path: Path):
    if not dir_path.is_dir():
        return []
    items = []
    for entry in sorted(dir_path.iterdir()):
        if entry.name.startswith(".") or entry.name == ".gitkeep":
            continue
        if entry.is_file():
            items.append(entry.name)
    return items


def find_theme_file(src_dir: Path, theme_name: str):
    candidate = src_dir / theme_name
    if candidate.is_file():
        return candidate
    return None


def install_themes(src_dir: Path, dest_dir: Path, mode: str, theme_name=None):
    if not src_dir.is_dir():
        raise FileNotFoundError(f"Theme source directory missing: {src_dir}")

    dest_dir.mkdir(parents=True, exist_ok=True)

    if theme_name:
        theme_file = find_theme_file(src_dir, theme_name)
        if theme_file is None:
            raise FileNotFoundError(f"Theme not found: {theme_name}")
        theme_files = [theme_file]
    else:
        theme_files = [p for p in src_dir.iterdir() if p.is_file() and p.name != ".gitkeep"]

    if not theme_files:
        raise FileNotFoundError("No themes found.")

    for src in theme_files:
        dest = dest_dir / src.name
        if dest.exists():
            if dest.is_symlink() and dest.resolve() == src.resolve():
                print(f"Already installed: {src.name}")
                continue
            print(f"Skipping existing file: {dest}")
            continue

        if mode == "copy":
            shutil.copy2(src, dest)
        else:
            os.symlink(src, dest)

        print(f"Installed: {src.name}")


def _trash_path(path: Path):
    if shutil.which("trash") is None:
        raise FileNotFoundError("'trash' is required for uninstall.")
    subprocess.run(["trash", str(path)], check=True)


def uninstall_themes(dest_dir: Path, src_dir: Path, theme_name=None):
    if not dest_dir.is_dir():
        print(f"No themes directory found: {dest_dir}")
        return

    if theme_name:
        targets = [dest_dir / theme_name]
    else:
        targets = [p for p in dest_dir.iterdir() if p.is_file() and p.name != ".gitkeep"]

    if not targets or all(not t.exists() for t in targets):
        print("No matching themes to uninstall.")
        return

    src_root = src_dir.resolve()

    for target in targets:
        if not target.exists() or target.name == ".gitkeep":
            continue
        if target.is_symlink():
            link_target = (target.parent / os.readlink(target)).resolve()
            try:
                link_target.relative_to(src_root)
            except ValueError:
                print(f"Skipping non-modus symlink: {target}")
                continue
            _trash_path(target)
            print(f"Removed: {target.name}")
        else:
            print(f"Skipping non-symlink file: {target}")
