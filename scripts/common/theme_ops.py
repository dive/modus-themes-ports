#!/usr/bin/env python3
"""Theme installation and management operations."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


def list_themes(
    dir_path: Path,
    theme_kind: str = "file",
    theme_ext: str = "",
    dir_suffix: str = ".yazi",
) -> list[str]:
    """List available themes in a directory.

    Args:
        dir_path: Directory containing themes.
        theme_kind: "file" for file-based themes, "dir" for directory-based.
        theme_ext: File extension for file-based themes.
        dir_suffix: Directory suffix for directory-based themes.

    Returns:
        List of theme names (without extensions/suffixes).
    """
    if not dir_path.is_dir():
        return []
    items: list[str] = []
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


def find_theme_file(
    src_dir: Path,
    theme_name: str,
    theme_ext: str = "",
) -> Path | None:
    """Find a theme file by name.

    Args:
        src_dir: Directory to search.
        theme_name: Theme name to find.
        theme_ext: Optional file extension.

    Returns:
        Path to the theme file, or None if not found.
    """
    candidate = src_dir / theme_name
    if candidate.is_file():
        return candidate
    if theme_ext and not theme_name.endswith(theme_ext):
        candidate = src_dir / f"{theme_name}{theme_ext}"
        if candidate.is_file():
            return candidate
    return None


def find_theme_dir(
    src_dir: Path,
    theme_name: str,
    dir_suffix: str = ".yazi",
) -> Path | None:
    """Find a theme directory by name.

    Args:
        src_dir: Directory to search.
        theme_name: Theme name to find.
        dir_suffix: Directory suffix.

    Returns:
        Path to the theme directory, or None if not found.
    """
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
    src_dir: Path,
    dest_dir: Path,
    mode: str,
    theme_name: str | None = None,
    theme_kind: str = "file",
    theme_ext: str = "",
    dir_suffix: str = ".yazi",
    theme_entry: str = "",
    symlink_entry_only: bool = False,
) -> None:
    """Install themes to a destination directory.

    Args:
        src_dir: Source directory containing themes.
        dest_dir: Destination directory for installed themes.
        mode: "link" for symlinks, "copy" for file copies.
        theme_name: Specific theme to install (all if None).
        theme_kind: "file" for file-based, "dir" for directory-based.
        theme_ext: File extension for file-based themes.
        dir_suffix: Directory suffix for directory-based themes.
        theme_entry: Entry file within directory themes.
        symlink_entry_only: Only symlink the entry file, not the whole dir.
    """
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

        # Handle symlink_entry_only mode for directory themes
        if theme_kind == "dir" and mode == "link" and symlink_entry_only and theme_entry:
            src_entry = src / theme_entry
            dest_entry = dest / theme_entry
            if dest_entry.exists():
                if dest_entry.is_symlink() and dest_entry.resolve() == src_entry.resolve():
                    print(f"Already installed: {src.name}")
                    continue
                print(f"Skipping existing file: {dest_entry}")
                continue
            dest.mkdir(parents=True, exist_ok=True)
            os.symlink(src_entry, dest_entry)
            print(f"Installed: {src.name}")
            continue

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


def _trash_path(path: Path) -> None:
    """Move a path to trash using the 'trash' command."""
    if shutil.which("trash") is None:
        raise FileNotFoundError("'trash' is required for uninstall.")
    subprocess.run(["trash", str(path)], check=True)


def uninstall_themes(
    dest_dir: Path,
    src_dir: Path,
    theme_name: str | None = None,
    theme_kind: str = "file",
    theme_ext: str = "",
    dir_suffix: str = ".yazi",
    theme_entry: str = "",
    symlink_entry_only: bool = False,
) -> None:
    """Uninstall themes from a destination directory.

    Only removes symlinks that point to the source directory.

    Args:
        dest_dir: Directory containing installed themes.
        src_dir: Original source directory (to verify symlinks).
        theme_name: Specific theme to uninstall (all if None).
        theme_kind: "file" for file-based, "dir" for directory-based.
        theme_ext: File extension for file-based themes.
        dir_suffix: Directory suffix for directory-based themes.
        theme_entry: Entry file within directory themes.
        symlink_entry_only: Only unlink the entry file, not the whole dir.
    """
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

        # Handle symlink_entry_only mode for directory themes
        if theme_kind == "dir" and symlink_entry_only and theme_entry:
            entry_path = target / theme_entry
            if entry_path.is_symlink():
                link_target = (entry_path.parent / os.readlink(entry_path)).resolve()
                try:
                    link_target.relative_to(src_root)
                except ValueError:
                    print(f"Skipping non-modus symlink: {entry_path}")
                    continue
                _trash_path(entry_path)
                # Remove the parent directory if empty
                if target.is_dir() and not any(target.iterdir()):
                    target.rmdir()
                print(f"Removed: {target.name}")
            elif entry_path.exists():
                print(f"Skipping non-symlink file: {entry_path}")
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
