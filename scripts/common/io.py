#!/usr/bin/env python3
"""File I/O utilities for Modus theme ports."""

from __future__ import annotations

import json
from pathlib import Path


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
    """Load a palette document and resolve palette references.

    Returns:
        A tuple of (theme_name, resolved_palette).
    """
    palette_path = Path(path)
    with palette_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError(f"Palette document must be an object: {palette_path}")
    missing_fields = [
        field for field in ("name", "license", "source", "palette") if field not in data
    ]
    if missing_fields:
        raise ValueError(
            f"Palette document missing fields: {', '.join(missing_fields)}: {palette_path}"
        )
    for field in ("name", "license", "source"):
        if not isinstance(data[field], str) or not data[field]:
            raise ValueError(f"Palette {field} must be a non-empty string: {palette_path}")

    palette = data["palette"]
    if not isinstance(palette, dict):
        raise ValueError(f"Palette must be an object: {palette_path}")
    invalid_entries = sorted(
        str(key)
        for key, value in palette.items()
        if not isinstance(key, str) or not isinstance(value, str)
    )
    if invalid_entries:
        raise ValueError(
            "Palette keys and values must be strings; invalid entries: "
            + ", ".join(invalid_entries)
        )
    return data["name"], resolve_palette(palette)


def write_output(path: str, content: str) -> Path:
    """Write content to a file, creating parent directories as needed."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not content.endswith("\n"):
        content += "\n"
    output_path.write_text(content, encoding="utf-8")
    return output_path
