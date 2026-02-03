#!/bin/sh
set -eu

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/../.." && pwd)

VENDOR_DIR="$REPO_ROOT/vendor/modus-themes"
OUT_DIR="$REPO_ROOT/palettes"

if [ ! -d "$VENDOR_DIR" ]; then
  echo "Error: missing subtree at $VENDOR_DIR" >&2
  echo "Run: scripts/core/update-subtree.sh" >&2
  exit 1
fi

if command -v emacs >/dev/null 2>&1; then
  EMACS_BIN=$(command -v emacs)
elif [ -x "$REPO_ROOT/.emacs-app/Emacs.app/Contents/MacOS/Emacs" ]; then
  EMACS_BIN="$REPO_ROOT/.emacs-app/Emacs.app/Contents/MacOS/Emacs"
else
  echo "Warning: Emacs not found." >&2
  echo "Run: scripts/core/fetch-emacs.sh" >&2
  exit 1
fi

mkdir -p "$OUT_DIR"

"$EMACS_BIN" -Q --batch \
  -l "$SCRIPT_DIR/extract-palettes.el" \
  --eval "(modus-themes-export-palettes \"$VENDOR_DIR\" \"$OUT_DIR\")"
