#!/usr/bin/env python3
"""Path utilities for Modus theme ports."""

from __future__ import annotations

import os
from pathlib import Path


def xdg_config_home() -> Path:
    """Return the XDG config home directory."""
    return Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))


def ghostty_config_dir() -> Path:
    """Return the Ghostty config directory."""
    return xdg_config_home() / "ghostty"


def ghostty_themes_dir() -> Path:
    """Return the Ghostty themes directory."""
    return xdg_config_home() / "ghostty" / "themes"


def lazygit_config_dir() -> Path:
    """Return the Lazygit config directory."""
    return xdg_config_home() / "lazygit"


def lazygit_themes_dir() -> Path:
    """Return the Lazygit themes directory."""
    return xdg_config_home() / "lazygit" / "themes"


def default_mapping(tool: str, repo_root: Path) -> Path:
    """Return the default mapping file path for a tool."""
    if tool == "ghostty":
        return repo_root / "mappings" / "base16" / "default.json"
    if tool == "lazygit":
        return repo_root / "mappings" / "lazygit" / "default.json"
    raise ValueError(f"Unknown tool: {tool}")


def default_output_dir(tool: str, repo_root: Path) -> Path:
    """Return the default output directory for a tool."""
    if tool == "ghostty":
        return repo_root / "ports" / "ghostty" / "themes"
    if tool == "lazygit":
        return repo_root / "ports" / "lazygit" / "themes"
    raise ValueError(f"Unknown tool: {tool}")


def spec_path(tool: str, repo_root: Path) -> Path:
    """Return the spec module path for a tool."""
    if tool == "ghostty":
        return repo_root / "scripts" / "tools" / "ghostty" / "spec.py"
    if tool == "lazygit":
        return repo_root / "scripts" / "tools" / "lazygit" / "spec.py"
    raise ValueError(f"Unknown tool: {tool}")
