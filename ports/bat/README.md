# bat Modus Themes

## Install
Install all themes (symlink mode):
- `python3 scripts/modus.py install --tool bat`

Install a single theme:
- `python3 scripts/modus.py install --tool bat --theme "modus-operandi"`

## Activate
Build bat's theme cache and select a theme:

```sh
bat cache --build
```

Add to `$XDG_CONFIG_HOME/bat/config`:

```ini
--theme="Modus Operandi"
```

## zsh + fzf Preview (macOS)

```sh
if (( $+commands[bat] )); then
  export FZF_CTRL_T_OPTS='--preview "bat --color=always --style=numbers --line-range=:500 --theme=\"$([[ $(defaults read -g AppleInterfaceStyle 2>/dev/null) == Dark ]] && echo Modus\ Vivendi || echo Modus\ Operandi)\" {}"'
fi
```

Themes are installed under `$XDG_CONFIG_HOME/bat/themes/`.
