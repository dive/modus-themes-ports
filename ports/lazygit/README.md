# Lazygit Modus Themes

## Update Flow
1. Update subtree and regenerate palettes + themes:
   - `scripts/update-subtree.sh`

2. If Emacs is not installed, download it once:
   - `scripts/fetch-emacs.sh`

3. Manually regenerate palettes:
   - `scripts/extract-palettes.sh`

4. Render Lazygit themes:
   - `scripts/render-lazygit-themes.sh`

## Install
Install all themes (symlink mode):
- `scripts/install-modus.sh install lazygit`

Install a single theme:
- `scripts/install-modus.sh install lazygit --theme "modus-operandi"`

Print the config block:
- `scripts/install-modus.sh print-config lazygit --theme "modus-operandi"`

## Uninstall
Remove installed symlinks:
- `scripts/install-modus.sh uninstall lazygit`

## Naming
All ports use kebab-case filenames with no extension (e.g. `modus-operandi`).
