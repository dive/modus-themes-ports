#!/bin/sh
set -eu

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/../../.." && pwd)

PALETTES_DIR="$REPO_ROOT/palettes"
MAPPING_FILE="$REPO_ROOT/mappings/lazygit/default.json"
OUT_DIR="$REPO_ROOT/ports/lazygit/themes"
SPEC_FILE="$REPO_ROOT/scripts/tools/lazygit/spec.py"
RENDER_PY="$REPO_ROOT/scripts/common/render.py"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 is required to render themes." >&2
  exit 1
fi

python3 "$RENDER_PY" \
  --palettes-dir "$PALETTES_DIR" \
  --mapping "$MAPPING_FILE" \
  --out-dir "$OUT_DIR" \
  --spec "$SPEC_FILE"
