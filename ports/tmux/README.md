# tmux Modus Themes

## Install

Install all themes (symlink mode):
- `python3 scripts/modus.py install --tool tmux`

Install a single theme:
- `python3 scripts/modus.py install --tool tmux --theme "modus-operandi"`

## Activate

Source the theme from your `~/.config/tmux/tmux.conf`:

```conf
source-file ~/.config/tmux/themes/modus-operandi.conf
```

Available themes:
- `modus-operandi` — light theme
- `modus-operandi-tinted` — light theme with subtle tinted backgrounds
- `modus-operandi-deuteranopia` — light theme optimized for red-green color deficiency
- `modus-operandi-tritanopia` — light theme optimized for blue-yellow color deficiency
- `modus-vivendi` — dark theme
- `modus-vivendi-tinted` — dark theme with subtle tinted backgrounds
- `modus-vivendi-deuteranopia` — dark theme optimized for red-green color deficiency
- `modus-vivendi-tritanopia` — dark theme optimized for blue-yellow color deficiency

## Notes

Themes are installed under `$XDG_CONFIG_HOME/tmux/themes/`.

The theme sets status bar, window status, pane border, message, popup, and copy-mode styles. It does not override key bindings or plugins.
