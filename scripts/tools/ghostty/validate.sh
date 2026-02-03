#!/bin/sh
set -eu

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/../../.." && pwd)

THEMES_DIR="$REPO_ROOT/ports/ghostty/themes"
SPEC_FILE="$REPO_ROOT/scripts/tools/ghostty/spec.py"
VALIDATE_PY="$REPO_ROOT/scripts/common/validate.py"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 is required to validate themes." >&2
  exit 1
fi

python3 "$VALIDATE_PY" \
  --themes-dir "$THEMES_DIR" \
  --spec "$SPEC_FILE"
