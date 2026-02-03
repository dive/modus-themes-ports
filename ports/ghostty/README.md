# Ghostty Modus Themes

## Update Flow
1. Update subtree and regenerate palettes + themes:
   - `scripts/core/update-subtree.sh`

2. If Emacs is not installed, download it once:
   - `scripts/core/fetch-emacs.sh`

3. Manually regenerate palettes:
   - `scripts/core/extract-palettes.sh`

4. Render Ghostty themes:
   - `scripts/tools/ghostty/render.sh`

## Install
Install all themes (symlink mode):
- `scripts/core/install-modus.sh install ghostty`

Install a single theme:
- `scripts/core/install-modus.sh install ghostty --theme "modus-operandi"`

Print the config line:
- `scripts/core/install-modus.sh print-config ghostty --theme "modus-operandi"`

## Config paths
Uses `XDG_CONFIG_HOME` (or `~/.config`) only.

## Naming
All ports use kebab-case filenames with no extension (e.g. `modus-operandi`). Use that name in `theme = ...`.

## Uninstall
Remove installed symlinks:
- `scripts/core/install-modus.sh uninstall ghostty`
