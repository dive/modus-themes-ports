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

## Notes

zsh + fzf preview (macOS):

```sh
if (( $+commands[bat] )); then
  export FZF_CTRL_T_OPTS='--preview "bat --color=always --style=numbers --line-range=:500 --theme=\"$([[ $(defaults read -g AppleInterfaceStyle 2>/dev/null) == Dark ]] && echo Modus\ Vivendi || echo Modus\ Operandi)\" {}"'
fi
```

Optional: align fzf UI colors with Modus (ANSI palette):

Pick the row matching your theme (Modus palette colors):

| Theme                         | `FZF_DEFAULT_OPTS`                                                                                                            |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `modus-operandi`              | `export FZF_DEFAULT_OPTS="$FZF_DEFAULT_OPTS --color=fg:#000000,fg+:#000000,bg:#ffffff,bg+:#f2f2f2,hl:#0031a9,hl+:#005e8b,info:#005e8b,prompt:#0031a9,spinner:#005e8b,pointer:#0031a9,marker:#006800,header:#595959"` |
| `modus-operandi-deuteranopia` | `export FZF_DEFAULT_OPTS="$FZF_DEFAULT_OPTS --color=fg:#000000,fg+:#000000,bg:#ffffff,bg+:#f2f2f2,hl:#0031a9,hl+:#005e8b,info:#005e8b,prompt:#0031a9,spinner:#005e8b,pointer:#0031a9,marker:#006800,header:#595959"` |
| `modus-operandi-tinted`       | `export FZF_DEFAULT_OPTS="$FZF_DEFAULT_OPTS --color=fg:#000000,fg+:#000000,bg:#fbf7f0,bg+:#efe9dd,hl:#0031a9,hl+:#00598b,info:#00598b,prompt:#0031a9,spinner:#00598b,pointer:#0031a9,marker:#006300,header:#595959"` |
| `modus-operandi-tritanopia`   | `export FZF_DEFAULT_OPTS="$FZF_DEFAULT_OPTS --color=fg:#000000,fg+:#000000,bg:#ffffff,bg+:#f2f2f2,hl:#0031a9,hl+:#005e8b,info:#005e8b,prompt:#0031a9,spinner:#005e8b,pointer:#0031a9,marker:#006800,header:#595959"` |
| `modus-vivendi`               | `export FZF_DEFAULT_OPTS="$FZF_DEFAULT_OPTS --color=fg:#ffffff,fg+:#ffffff,bg:#000000,bg+:#1e1e1e,hl:#2fafff,hl+:#00d3d0,info:#00d3d0,prompt:#2fafff,spinner:#00d3d0,pointer:#2fafff,marker:#44bc44,header:#989898"` |
| `modus-vivendi-deuteranopia`  | `export FZF_DEFAULT_OPTS="$FZF_DEFAULT_OPTS --color=fg:#ffffff,fg+:#ffffff,bg:#000000,bg+:#1e1e1e,hl:#2fafff,hl+:#00d3d0,info:#00d3d0,prompt:#2fafff,spinner:#00d3d0,pointer:#2fafff,marker:#44bc44,header:#989898"` |
| `modus-vivendi-tinted`        | `export FZF_DEFAULT_OPTS="$FZF_DEFAULT_OPTS --color=fg:#ffffff,fg+:#ffffff,bg:#0d0e1c,bg+:#1d2235,hl:#2fafff,hl+:#00d3d0,info:#00d3d0,prompt:#2fafff,spinner:#00d3d0,pointer:#2fafff,marker:#44bc44,header:#989898"` |
| `modus-vivendi-tritanopia`    | `export FZF_DEFAULT_OPTS="$FZF_DEFAULT_OPTS --color=fg:#ffffff,fg+:#ffffff,bg:#000000,bg+:#1e1e1e,hl:#2fafff,hl+:#00d3d0,info:#00d3d0,prompt:#2fafff,spinner:#00d3d0,pointer:#2fafff,marker:#44bc44,header:#989898"` |

Themes are installed under `$XDG_CONFIG_HOME/bat/themes/`.
