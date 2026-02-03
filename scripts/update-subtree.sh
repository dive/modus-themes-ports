#!/bin/sh
set -eu

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)

REMOTE_URL="https://github.com/protesilaos/modus-themes"
PREFIX="vendor/modus-themes"

if ! command -v git >/dev/null 2>&1; then
  echo "Error: git is required." >&2
  exit 1
fi

DEFAULT_BRANCH=$(git ls-remote --symref "$REMOTE_URL" HEAD 2>/dev/null | awk '/^ref:/ {sub("refs/heads/","",$2); print $2; exit}')
BRANCH=${DEFAULT_BRANCH:-master}

if [ ! -d "$REPO_ROOT/$PREFIX" ]; then
  echo "Adding subtree $REMOTE_URL ($BRANCH)..."
  git subtree add --prefix "$PREFIX" "$REMOTE_URL" "$BRANCH" --squash
else
  echo "Updating subtree $REMOTE_URL ($BRANCH)..."
  git subtree pull --prefix "$PREFIX" "$REMOTE_URL" "$BRANCH" --squash
fi

"$SCRIPT_DIR/extract-palettes.sh"
"$SCRIPT_DIR/render-ghostty-themes.sh"
