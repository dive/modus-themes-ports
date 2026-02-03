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

Optional: align fzf UI colors with Modus (ANSI palette):

```sh
export FZF_DEFAULT_OPTS="$FZF_DEFAULT_OPTS --color=fg:7,fg+:15,bg:0,bg+:8,hl:4,hl+:14,info:6,prompt:4,spinner:6,pointer:4,marker:2,header:8"
```

Themes are installed under `$XDG_CONFIG_HOME/bat/themes/`.
