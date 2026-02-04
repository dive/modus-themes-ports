# Pi Modus Themes

## Install
Install all themes (symlink mode):
- `python3 scripts/modus.py install --tool pi`

Install a single theme:
- `python3 scripts/modus.py install --tool pi --theme "modus-operandi"`

## Activate
Set the theme in `~/.pi/agent/settings.json` (or `.pi/settings.json`):
`"theme": "modus-operandi"`

You can also select themes via `/settings` in the UI.

## Notes
Themes are installed under `~/.pi/agent/themes/`.
Pi also loads project themes from `.pi/themes/`.
Docs: https://raw.githubusercontent.com/badlogic/pi-mono/main/packages/coding-agent/docs/themes.md
