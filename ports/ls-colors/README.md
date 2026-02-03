# LS_COLORS Modus Themes

## Install
Install all themes (symlink mode):
- `python3 scripts/modus.py install --tool ls-colors`

Install a single theme:
- `python3 scripts/modus.py install --tool ls-colors --theme "modus-operandi"`

## Activate (zsh)
Manual source:

```sh
source "$XDG_CONFIG_HOME/ls-colors/modus-vivendi"
```

macOS auto-switch:

```sh
if [[ $(defaults read -g AppleInterfaceStyle 2>/dev/null) == "Dark" ]]; then
  source "$XDG_CONFIG_HOME/ls-colors/modus-vivendi"
else
  source "$XDG_CONFIG_HOME/ls-colors/modus-operandi"
fi
```

Flavors are installed under `$XDG_CONFIG_HOME/ls-colors/`.
