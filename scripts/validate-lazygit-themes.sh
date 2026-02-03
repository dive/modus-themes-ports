#!/bin/sh
set -eu

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)

THEMES_DIR="$REPO_ROOT/ports/lazygit/themes"

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

required_keys = {
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
}

files = sorted(glob.glob(os.path.join(sys.argv[1], "*")))
if not files:
    raise SystemExit("No theme files found to validate.")

errors = 0
validated = 0
key_re = re.compile(r"^\s{4}([A-Za-z]+):\s*$")

for path in files:
    if os.path.isdir(path) or os.path.basename(path) == ".gitkeep":
        continue

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    found_keys = set()
    in_gui = False
    in_theme = False

    for line in lines:
        if line.strip().startswith("#") or not line.strip():
            continue
        if line.startswith("gui:"):
            in_gui = True
            in_theme = False
            continue
        if in_gui and line.startswith("  theme:"):
            in_theme = True
            continue
        if in_theme:
            m = key_re.match(line)
            if m:
                found_keys.add(m.group(1))

    missing = required_keys - found_keys
    if missing:
        errors += 1
        print(f"Invalid theme: {path}")
        print(f"  Missing keys: {', '.join(sorted(missing))}")
        continue

    validated += 1

if errors:
    raise SystemExit(f"Validation failed for {errors} theme(s).")

print(f"Validated {validated} theme(s).")
PY
