#!/bin/sh
set -eu

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)

PALETTES_DIR="$REPO_ROOT/palettes"
MAPPING_DIR="$REPO_ROOT/mappings/base16"
OUT_DIR="$REPO_ROOT/ports/ghostty/themes"
DEFAULT_MAPPING="$MAPPING_DIR/default.json"

if [ ! -d "$PALETTES_DIR" ]; then
  echo "Error: palettes directory missing: $PALETTES_DIR" >&2
  exit 1
fi

if [ ! -f "$DEFAULT_MAPPING" ]; then
  echo "Error: default mapping missing: $DEFAULT_MAPPING" >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 is required to render themes." >&2
  exit 1
fi

mkdir -p "$OUT_DIR"

python3 - "$PALETTES_DIR" "$MAPPING_DIR" "$OUT_DIR" "$DEFAULT_MAPPING" <<'PY'
import json
import os
import sys

palettes_dir, mapping_dir, out_dir, default_mapping = sys.argv[1:5]

with open(default_mapping, "r", encoding="utf-8") as f:
    default_map = json.load(f)

required_map_keys = [
    "background",
    "foreground",
    "cursor-color",
    "selection-background",
    "selection-foreground",
    "palette",
]

for key in required_map_keys:
    if key not in default_map:
        raise SystemExit(f"Missing mapping key: {key}")


def load_palette(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "palette" in data:
        return data.get("name", os.path.splitext(os.path.basename(path))[0]), data["palette"]
    return os.path.splitext(os.path.basename(path))[0], data


def load_mapping(theme_name: str):
    candidate = os.path.join(mapping_dir, f"{theme_name}.json")
    if os.path.isfile(candidate):
        with open(candidate, "r", encoding="utf-8") as f:
            return json.load(f)
    return default_map


def resolve_color(palette, key: str) -> str:
    value = palette.get(key)
    if value is None:
        raise KeyError(key)
    return value


palette_files = [
    p for p in sorted(os.listdir(palettes_dir))
    if p.endswith(".json") and not p.startswith(".")
]

if not palette_files:
    raise SystemExit("No palettes found. Run scripts/extract-palettes.sh")

for filename in palette_files:
    path = os.path.join(palettes_dir, filename)
    theme_name, palette = load_palette(path)
    mapping = load_mapping(theme_name)
    out_path = os.path.join(out_dir, theme_name)

    lines = []
    for key in required_map_keys[:-1]:
        palette_key = mapping[key]
        color = resolve_color(palette, palette_key)
        lines.append(f"{key} = {color}")

    palette_map = mapping["palette"]
    for i in range(16):
        key = str(i)
        palette_key = palette_map.get(key)
        if palette_key is None:
            raise KeyError(f"palette[{key}]")
        color = resolve_color(palette, palette_key)
        lines.append(f"palette = {i}={color}")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Wrote {out_path}")
PY
