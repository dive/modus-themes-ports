# Yazi Modus Themes

## Install
Install all themes (symlink mode):
- `python3 scripts/modus.py install --tool yazi`

Install a single theme:
- `python3 scripts/modus.py install --tool yazi --theme "modus-operandi"`

## Activate
Add the flavor to `theme.toml`:

```toml
[flavor]
dark = "modus-vivendi"
light = "modus-operandi"
```

Flavors are installed under `$XDG_CONFIG_HOME/yazi/flavors/`.

## Notes
This port ships `flavor.toml` and `tmtheme.xml` for each flavor.
