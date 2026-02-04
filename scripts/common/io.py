#!/usr/bin/env python3
import importlib.util
import json
import os
from pathlib import Path


def load_spec(path: str):
    spec_path = Path(path)
    if not spec_path.is_file():
        raise FileNotFoundError(f"Spec not found: {spec_path}")
    spec = importlib.util.spec_from_file_location("tool_spec", str(spec_path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load spec: {spec_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_mapping(path: str):
    mapping_path = Path(path)
    if not mapping_path.is_file():
        raise FileNotFoundError(f"Mapping not found: {mapping_path}")
    with mapping_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _resolve_palette_value(palette: dict, key: str, resolved: dict, stack: list):
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


def resolve_palette(palette: dict) -> dict:
    resolved = {}
    for key in palette:
        _resolve_palette_value(palette, key, resolved, [])
    return resolved


def load_palette(path: str):
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


def write_output(path: str, content: str):
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not content.endswith("\n"):
        content += "\n"
    output_path.write_text(content, encoding="utf-8")
    return output_path
