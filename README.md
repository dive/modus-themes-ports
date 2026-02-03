# modus-themes-ports
Modus theme ports for the tools & editors in my workflow

## Requirements
- `git` with `git subtree`
- `emacs` (system) or `scripts/fetch-emacs.sh` (macOS)
- `python3` (render + validation)

## Quick start
1. Update subtree + generate palettes + render themes:
   - `scripts/update-subtree.sh`

2. If you do not have Emacs installed:
   - `scripts/fetch-emacs.sh`

3. Install Ghostty themes:
   - `scripts/install-modus.sh install ghostty`

## Scripts
- `scripts/update-subtree.sh`: update `vendor/modus-themes`, regenerate palettes, and render Ghostty themes
- `scripts/fetch-emacs.sh`: download and cache Emacs.app in `.emacs-app/`
- `scripts/extract-palettes.sh`: generate `palettes/*.json` from the subtree
- `scripts/render-ghostty-themes.sh`: render `ports/ghostty/themes/*.theme`
- `scripts/install-modus.sh`: install, uninstall, list themes
- `scripts/validate-ghostty-themes.sh`: validate Ghostty theme files

## Naming
All ported theme filenames use kebab-case with no extension (e.g. `modus-operandi`). Use the kebab-case name in tool configs.
