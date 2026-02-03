#!/usr/bin/env python3
import os
from pathlib import Path


def xdg_config_home() -> Path:
    return Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))


def ghostty_config_dir() -> Path:
    return xdg_config_home() / "ghostty"


def ghostty_themes_dir() -> Path:
    return xdg_config_home() / "ghostty" / "themes"


def lazygit_config_dir() -> Path:
    return xdg_config_home() / "lazygit"


def lazygit_themes_dir() -> Path:
    return xdg_config_home() / "lazygit" / "themes"


def default_mapping(tool: str, repo_root: Path) -> Path:
    if tool == "ghostty":
        return repo_root / "mappings" / "base16" / "default.json"
    if tool == "lazygit":
        return repo_root / "mappings" / "lazygit" / "default.json"
    raise ValueError(f"Unknown tool: {tool}")


def default_output_dir(tool: str, repo_root: Path) -> Path:
    if tool == "ghostty":
        return repo_root / "ports" / "ghostty" / "themes"
    if tool == "lazygit":
        return repo_root / "ports" / "lazygit" / "themes"
    raise ValueError(f"Unknown tool: {tool}")


def spec_path(tool: str, repo_root: Path) -> Path:
    if tool == "ghostty":
        return repo_root / "scripts" / "tools" / "ghostty" / "spec.py"
    if tool == "lazygit":
        return repo_root / "scripts" / "tools" / "lazygit" / "spec.py"
    raise ValueError(f"Unknown tool: {tool}")
