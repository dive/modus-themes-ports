# Ghostty Modus Themes

## Update Flow
1. Update subtree and regenerate palettes + themes:
   - `python3 scripts/modus.py update-subtree`

2. If Emacs is not installed, download it once:
   - `python3 scripts/modus.py fetch-emacs`

3. Manually regenerate palettes:
   - `python3 scripts/modus.py extract-palettes`

4. Render Ghostty themes:
   - `python3 scripts/modus.py render --tool ghostty`

Render all tools:
- `python3 scripts/modus.py render --tool all`

## Install
Install all themes (symlink mode):
- `python3 scripts/modus.py install --tool ghostty`

Install a single theme:
- `python3 scripts/modus.py install --tool ghostty --theme "modus-operandi"`

Print the config line:
- `python3 scripts/modus.py print-config --tool ghostty --theme "modus-operandi"`

## Config paths
Uses `XDG_CONFIG_HOME` (or `~/.config`) only.

## Naming
All ports use kebab-case filenames with no extension (e.g. `modus-operandi`). Use that name in `theme = ...`.

## Uninstall
Remove installed symlinks:
- `python3 scripts/modus.py uninstall --tool ghostty`
