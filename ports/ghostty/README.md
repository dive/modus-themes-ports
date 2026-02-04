# Ghostty Modus Themes

## Install
Install all themes (symlink mode):
- `python3 scripts/modus.py install --tool ghostty`

Install a single theme:
- `python3 scripts/modus.py install --tool ghostty --theme "modus-operandi"`

## Activate
Set the theme in Ghostty config:
`theme = modus-operandi`

## Notes
Themes are installed under `$XDG_CONFIG_HOME/ghostty/themes/`.
Ghostty uses Modus terminal palette (`fg-term-*` and `fg-term-*-bright`) for ANSI slots.
