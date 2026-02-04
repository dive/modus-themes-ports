# OpenCode Modus Themes

## Install
Install all themes (symlink mode):
- `python3 scripts/modus.py install --tool opencode`

Install a single theme:
- `python3 scripts/modus.py install --tool opencode --theme "modus-operandi"`

## Activate
Set the theme in your OpenCode config (e.g. `~/.config/opencode/opencode.json`):
`"theme": "modus-operandi"`

## Notes
Themes are installed under `$XDG_CONFIG_HOME/opencode/themes/`.
OpenCode also loads project themes from `.opencode/themes/`.
