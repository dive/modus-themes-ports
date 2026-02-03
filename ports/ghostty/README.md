# Ghostty Modus Themes

## Update Flow
1. Update subtree and regenerate palettes + themes:
   - `scripts/update-subtree.sh`

2. If Emacs is not installed, download it once:
   - `scripts/fetch-emacs.sh`

3. Manually regenerate palettes:
   - `scripts/extract-palettes.sh`

4. Render Ghostty themes:
   - `scripts/render-ghostty-themes.sh`

## Install
Install all themes (symlink mode):
- `scripts/install-modus.sh install ghostty`

Install a single theme:
- `scripts/install-modus.sh install ghostty --theme "Modus Operandi"`

Print the config line:
- `scripts/install-modus.sh print-config ghostty --theme "Modus Operandi"`

## Uninstall
Remove installed symlinks:
- `scripts/install-modus.sh uninstall ghostty`
