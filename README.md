# modus-themes-ports
Modus theme ports for the tools & editors in my workflow

## Requirements
- `git` with `git subtree`
- `emacs` (system) or `scripts/core/fetch-emacs.sh` (macOS)
- `python3` (render + validation)

## Quick start
1. Update subtree + generate palettes + render themes:
   - `scripts/core/update-subtree.sh`

2. If you do not have Emacs installed:
   - `scripts/core/fetch-emacs.sh`

3. Install Ghostty themes:
   - `scripts/core/install-modus.sh install ghostty`

## Scripts
- `scripts/core/update-subtree.sh`: update `vendor/modus-themes`, regenerate palettes, and render themes
- `scripts/core/fetch-emacs.sh`: download and cache Emacs.app in `.emacs-app/`
- `scripts/core/extract-palettes.sh`: generate `palettes/*.json` from the subtree
- `scripts/tools/ghostty/render.sh`: render `ports/ghostty/themes/*`
- `scripts/tools/lazygit/render.sh`: render `ports/lazygit/themes/*`
- `scripts/core/install-modus.sh`: install, uninstall, list themes
- `scripts/tools/ghostty/validate.sh`: validate Ghostty theme files
- `scripts/tools/lazygit/validate.sh`: validate Lazygit theme files

## Naming
All ported theme filenames use kebab-case with no extension (e.g. `modus-operandi`). Use the kebab-case name in tool configs.

## Config paths
All tooling defaults to `XDG_CONFIG_HOME` (or `~/.config`) and does not use `~/Library/Application Support`.
