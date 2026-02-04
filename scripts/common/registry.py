#!/usr/bin/env python3
"""Tool registry for Modus theme ports."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_registry(repo_root: Path) -> dict[str, dict[str, Any]]:
    """Load the tool registry from port manifests.

    Args:
        repo_root: Repository root directory.

    Returns:
        Dictionary mapping tool names to their manifest data.
    """
    ports_dir = repo_root / "ports"
    if not ports_dir.is_dir():
        raise FileNotFoundError(f"Ports directory missing: {ports_dir}")

    registry: dict[str, dict[str, Any]] = {}
    for manifest_path in sorted(ports_dir.glob("*/*-port.json")):
        with manifest_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        tool = data.get("tool")
        if not tool:
            raise ValueError(f"Missing tool name in {manifest_path}")
        if tool in registry:
            raise ValueError(f"Duplicate tool entry: {tool}")
        registry[tool] = data | {"_manifest_path": str(manifest_path)}

    return registry


def get_tool(registry: dict[str, dict[str, Any]], tool: str) -> dict[str, Any]:
    """Get a tool's manifest from the registry.

    Args:
        registry: The loaded tool registry.
        tool: Tool name to look up.

    Returns:
        The tool's manifest data.

    Raises:
        KeyError: If the tool is not in the registry.
    """
    if tool not in registry:
        raise KeyError(f"Unknown tool: {tool}")
    return registry[tool]
