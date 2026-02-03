# Zed Modus Themes

## Install
Install all themes (symlink mode):
- `python3 scripts/modus.py install --tool zed`

Install a single theme:
- `python3 scripts/modus.py install --tool zed --theme "modus-operandi"`

## Activate
Add to `$XDG_CONFIG_HOME/zed/settings.json`:

```json
{
  "theme": {
    "mode": "system",
    "light": "Modus Operandi",
    "dark": "Modus Vivendi"
  }
}
```

## Notes
Themes are installed under `$XDG_CONFIG_HOME/zed/themes/`.
