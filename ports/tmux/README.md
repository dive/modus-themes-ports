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

See the repository's [theme variant table](../../README.md#theme-variants) for the complete list of light, dark, tinted, and color-deficiency variants.

## Notes

Themes are installed under `$XDG_CONFIG_HOME/tmux/themes/`.

The theme sets status bar, window status, pane border, message, popup, and copy-mode styles. It does not override key bindings or plugins.
