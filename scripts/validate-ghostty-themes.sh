#!/bin/sh
set -eu

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)

THEMES_DIR="$REPO_ROOT/ports/ghostty/themes"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 is required to validate themes." >&2
  exit 1
fi

if [ ! -d "$THEMES_DIR" ]; then
  echo "Error: themes directory missing: $THEMES_DIR" >&2
  exit 1
fi

python3 - "$THEMES_DIR" <<'PY'
import glob
import os
import re
import sys

themes_dir = sys.argv[1]
files = sorted(glob.glob(os.path.join(themes_dir, "*.theme")))
if not files:
    raise SystemExit("No .theme files found to validate.")

required_keys = {
    "background",
    "foreground",
    "cursor-color",
    "selection-background",
    "selection-foreground",
}

palette_re = re.compile(r"^palette\s*=\s*(\d+)\s*=\s*(#?[0-9A-Fa-f]{6,8})$")
key_re = re.compile(r"^([a-zA-Z-]+)\s*=\s*(#?[0-9A-Fa-f]{6,8})$")

errors = 0
for path in files:
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]

    found_keys = set()
    palette = {}

    for line in lines:
        m = palette_re.match(line)
        if m:
            palette[int(m.group(1))] = m.group(2)
            continue
        m = key_re.match(line)
        if m:
            found_keys.add(m.group(1))
            continue

    missing_keys = required_keys - found_keys
    missing_palette = [i for i in range(16) if i not in palette]

    if missing_keys or missing_palette:
        errors += 1
        print(f"Invalid theme: {path}")
        if missing_keys:
            print(f"  Missing keys: {', '.join(sorted(missing_keys))}")
        if missing_palette:
            print(f"  Missing palette indices: {', '.join(str(i) for i in missing_palette)}")

if errors:
    raise SystemExit(f"Validation failed for {errors} theme(s).")

print(f"Validated {len(files)} theme(s).")
PY
