#!/usr/bin/env python3
import os
import shutil
import subprocess
from pathlib import Path


def list_themes(dir_path: Path, theme_kind: str = "file", theme_ext: str = "", dir_suffix: str = ".yazi"):
    if not dir_path.is_dir():
        return []
    items = []
    for entry in sorted(dir_path.iterdir()):
        if entry.name.startswith(".") or entry.name == ".gitkeep":
            continue
        if theme_kind == "dir":
            if entry.is_dir():
                name = entry.name
                if dir_suffix and name.endswith(dir_suffix):
                    name = name[: -len(dir_suffix)]
                items.append(name)
        else:
            if entry.is_file():
                name = entry.name
                if theme_ext and name.endswith(theme_ext):
                    name = name[: -len(theme_ext)]
                items.append(name)
    return items


def find_theme_file(src_dir: Path, theme_name: str, theme_ext: str = ""):
    candidate = src_dir / theme_name
    if candidate.is_file():
        return candidate
    if theme_ext and not theme_name.endswith(theme_ext):
        candidate = src_dir / f"{theme_name}{theme_ext}"
        if candidate.is_file():
            return candidate
    return None


def find_theme_dir(src_dir: Path, theme_name: str, dir_suffix: str = ".yazi"):
    if dir_suffix and theme_name.endswith(dir_suffix):
        candidate = src_dir / theme_name
    elif dir_suffix:
        candidate = src_dir / f"{theme_name}{dir_suffix}"
    else:
        candidate = src_dir / theme_name
    if candidate.is_dir():
        return candidate
    return None


def install_themes(
    src_dir: Path, dest_dir: Path, mode: str, theme_name=None, theme_kind: str = "file", theme_ext: str = "", dir_suffix: str = ".yazi"
):
    if not src_dir.is_dir():
        raise FileNotFoundError(f"Theme source directory missing: {src_dir}")

    dest_dir.mkdir(parents=True, exist_ok=True)

    if theme_kind == "dir":
        if theme_name:
            theme_dir = find_theme_dir(src_dir, theme_name, dir_suffix)
            if theme_dir is None:
                raise FileNotFoundError(f"Theme not found: {theme_name}")
            theme_files = [theme_dir]
        else:
            if dir_suffix:
                theme_files = [p for p in src_dir.iterdir() if p.is_dir() and p.name.endswith(dir_suffix)]
            else:
                theme_files = [p for p in src_dir.iterdir() if p.is_dir() and not p.name.startswith(".")]
    else:
        if theme_name:
            theme_file = find_theme_file(src_dir, theme_name, theme_ext)
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
            if src.is_dir():
                shutil.copytree(src, dest)
            else:
                shutil.copy2(src, dest)
        else:
            os.symlink(src, dest)

        print(f"Installed: {src.name}")


def _trash_path(path: Path):
    if shutil.which("trash") is None:
        raise FileNotFoundError("'trash' is required for uninstall.")
    subprocess.run(["trash", str(path)], check=True)


def uninstall_themes(dest_dir: Path, src_dir: Path, theme_name=None, theme_kind: str = "file", theme_ext: str = "", dir_suffix: str = ".yazi"):
    if not dest_dir.is_dir():
        print(f"No themes directory found: {dest_dir}")
        return

    if theme_kind == "dir":
        if theme_name:
            if dir_suffix:
                name = theme_name if theme_name.endswith(dir_suffix) else f"{theme_name}{dir_suffix}"
            else:
                name = theme_name
            targets = [dest_dir / name]
        else:
            if dir_suffix:
                targets = [p for p in dest_dir.iterdir() if p.is_dir() and p.name.endswith(dir_suffix)]
            else:
                targets = [p for p in dest_dir.iterdir() if p.is_dir() and not p.name.startswith(".")]
    else:
        if theme_name:
            name = theme_name
            if theme_ext and not name.endswith(theme_ext):
                name = f"{name}{theme_ext}"
            targets = [dest_dir / name]
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
