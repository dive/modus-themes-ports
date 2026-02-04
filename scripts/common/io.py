#!/usr/bin/env python3
"""File I/O utilities for Modus theme ports."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType
from typing import Any


def load_spec(path: str) -> ModuleType:
    """Load a Python spec module from the given path."""
    spec_path = Path(path)
    if not spec_path.is_file():
        raise FileNotFoundError(f"Spec not found: {spec_path}")
    spec = importlib.util.spec_from_file_location("tool_spec", str(spec_path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load spec: {spec_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_mapping(path: str) -> dict[str, Any]:
    """Load a JSON mapping file."""
    mapping_path = Path(path)
    if not mapping_path.is_file():
        raise FileNotFoundError(f"Mapping not found: {mapping_path}")
    with mapping_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _resolve_palette_value(
    palette: dict[str, str],
    key: str,
    resolved: dict[str, str],
    stack: list[str],
) -> str:
    """Resolve a single palette value, detecting circular references."""
    if key in resolved:
        return resolved[key]
    if key in stack:
        cycle = " -> ".join(stack + [key])
        raise ValueError(f"Circular palette reference: {cycle}")
    stack.append(key)
    value = palette[key]
    if isinstance(value, str) and value in palette:
        value = _resolve_palette_value(palette, value, resolved, stack)
    resolved[key] = value
    stack.pop()
    return value


def resolve_palette(palette: dict[str, str]) -> dict[str, str]:
    """Resolve all palette references to their final values."""
    resolved: dict[str, str] = {}
    for key in palette:
        _resolve_palette_value(palette, key, resolved, [])
    return resolved


def load_palette(path: str) -> tuple[str, dict[str, str]]:
    """Load a palette JSON file and resolve all references.

    Returns:
        A tuple of (theme_name, resolved_palette).
    """
    palette_path = Path(path)
    with palette_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "palette" in data:
        name = data.get("name") or palette_path.stem
        palette = data["palette"]
    else:
        name = palette_path.stem
        palette = data
    if not isinstance(palette, dict):
        raise ValueError(f"Palette must be an object: {palette_path}")
    # NOTE: Resolve palette references so rendered themes never contain alias names.
    return name, resolve_palette(palette)


def write_output(path: str, content: str) -> Path:
    """Write content to a file, creating parent directories as needed."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not content.endswith("\n"):
        content += "\n"
    output_path.write_text(content, encoding="utf-8")
    return output_path
