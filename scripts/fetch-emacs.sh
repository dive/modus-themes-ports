#!/bin/sh
set -eu

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)

EMACS_DIR="$REPO_ROOT/.emacs-app"
EMACS_APP="$EMACS_DIR/Emacs.app"
DMG_NAME="Emacs-30.2-1-universal.dmg"
DMG_URL="https://emacsformacosx.com/emacs-builds/Emacs-30.2-1-universal.dmg"
DMG_PATH="$EMACS_DIR/$DMG_NAME"

if [ -d "$EMACS_APP" ]; then
  echo "Emacs.app already present: $EMACS_APP"
  exit 0
fi

if ! command -v curl >/dev/null 2>&1; then
  echo "Error: curl is required to download Emacs." >&2
  exit 1
fi

if ! command -v hdiutil >/dev/null 2>&1; then
  echo "Error: hdiutil is required to mount the DMG." >&2
  exit 1
fi

mkdir -p "$EMACS_DIR"

if [ ! -f "$DMG_PATH" ]; then
  echo "Downloading $DMG_NAME..."
  curl -L -o "$DMG_PATH" "$DMG_URL"
else
  echo "DMG already present: $DMG_PATH"
fi

MOUNT_POINT=$(hdiutil attach -nobrowse -readonly "$DMG_PATH" | awk 'END{print $3}')
if [ -z "$MOUNT_POINT" ]; then
  echo "Error: failed to mount DMG." >&2
  exit 1
fi

cleanup() {
  hdiutil detach "$MOUNT_POINT" -quiet >/dev/null 2>&1 || true
}
trap cleanup EXIT

if [ ! -d "$MOUNT_POINT/Emacs.app" ]; then
  echo "Error: Emacs.app not found in DMG." >&2
  exit 1
fi

echo "Copying Emacs.app to $EMACS_APP"
ditto "$MOUNT_POINT/Emacs.app" "$EMACS_APP"

echo "Emacs.app installed to $EMACS_APP"
