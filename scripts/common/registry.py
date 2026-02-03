#!/usr/bin/env python3
import json
from pathlib import Path


def load_registry(repo_root: Path):
    ports_dir = repo_root / "ports"
    if not ports_dir.is_dir():
        raise FileNotFoundError(f"Ports directory missing: {ports_dir}")

    registry = {}
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


def get_tool(registry: dict, tool: str):
    if tool not in registry:
        raise KeyError(f"Unknown tool: {tool}")
    return registry[tool]
