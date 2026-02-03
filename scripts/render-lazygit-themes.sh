#!/bin/sh
set -eu

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)

PALETTES_DIR="$REPO_ROOT/palettes"
MAPPING_DIR="$REPO_ROOT/mappings/lazygit"
OUT_DIR="$REPO_ROOT/ports/lazygit/themes"
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

python3 - "$PALETTES_DIR" "$DEFAULT_MAPPING" "$OUT_DIR" <<'PY'
import json
import os
import sys

palettes_dir, default_mapping, out_dir = sys.argv[1:4]

with open(default_mapping, "r", encoding="utf-8") as f:
    mapping = json.load(f)

order = [
    "activeBorderColor",
    "inactiveBorderColor",
    "searchingActiveBorderColor",
    "optionsTextColor",
    "selectedLineBgColor",
    "inactiveViewSelectedLineBgColor",
    "cherryPickedCommitFgColor",
    "cherryPickedCommitBgColor",
    "markedBaseCommitFgColor",
    "markedBaseCommitBgColor",
    "unstagedChangesColor",
    "defaultFgColor",
]

for key in order:
    if key not in mapping:
        raise SystemExit(f"Missing mapping key: {key}")


def load_palette(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "palette" in data:
        return data.get("name", os.path.splitext(os.path.basename(path))[0]), data["palette"]
    return os.path.splitext(os.path.basename(path))[0], data


def resolve_token(palette, token: str) -> str:
    if token in palette:
        return palette[token]
    return token


def yaml_value(value: str) -> str:
    if value.startswith("#"):
        return f"\"{value}\""
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

    lines = ["gui:", "  theme:"]
    for key in order:
        tokens = mapping[key]
        if not isinstance(tokens, list):
            raise SystemExit(f"Mapping for {key} must be a list")
        lines.append(f"    {key}:")
        for token in tokens:
            value = resolve_token(palette, token)
            lines.append(f"      - {yaml_value(value)}")

    out_path = os.path.join(out_dir, theme_name)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Wrote {out_path}")
PY
