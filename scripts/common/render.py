#!/usr/bin/env python3
import argparse
import importlib.util
import json
import os
import sys


def load_spec(path: str):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Spec not found: {path}")
    spec = importlib.util.spec_from_file_location("tool_spec", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load spec: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "render"):
        raise AttributeError("Spec missing render(theme_name, palette, mapping)")
    return module


def load_palette(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "palette" in data:
        name = data.get("name") or os.path.splitext(os.path.basename(path))[0]
        palette = data["palette"]
    else:
        name = os.path.splitext(os.path.basename(path))[0]
        palette = data
    if not isinstance(palette, dict):
        raise ValueError(f"Palette must be an object: {path}")
    return name, palette


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--palettes-dir", required=True)
    parser.add_argument("--mapping", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--spec", required=True)
    args = parser.parse_args()

    if not os.path.isdir(args.palettes_dir):
        print(f"Error: palettes directory missing: {args.palettes_dir}", file=sys.stderr)
        return 1

    if not os.path.isfile(args.mapping):
        print(f"Error: mapping file missing: {args.mapping}", file=sys.stderr)
        return 1

    with open(args.mapping, "r", encoding="utf-8") as f:
        mapping = json.load(f)

    spec = load_spec(args.spec)

    os.makedirs(args.out_dir, exist_ok=True)

    palette_files = [
        p for p in sorted(os.listdir(args.palettes_dir))
        if p.endswith(".json") and not p.startswith(".")
    ]

    if not palette_files:
        print("Error: no palettes found. Run scripts/core/extract-palettes.sh", file=sys.stderr)
        return 1

    for filename in palette_files:
        path = os.path.join(args.palettes_dir, filename)
        theme_name, palette = load_palette(path)
        content = spec.render(theme_name, palette, mapping)
        if not content.endswith("\n"):
            content += "\n"
        out_path = os.path.join(args.out_dir, theme_name)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Wrote {out_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
