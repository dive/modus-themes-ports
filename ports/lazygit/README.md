# Lazygit Modus Themes

## Install
Install all themes (symlink mode):
- `python3 scripts/modus.py install --tool lazygit`

Install a single theme:
- `python3 scripts/modus.py install --tool lazygit --theme "modus-operandi"`

## Config override
Lazygit does not automatically load per-theme files. You must explicitly pass config paths via `--use-config-file`.

Docs:
- `https://github.com/jesseduffield/lazygit/blob/master/docs/Config.md#overriding-default-config-file-location`

Themes are installed under `$XDG_CONFIG_HOME/lazygit/themes/`. You can symlink one to `light-mode.yml`/`dark-mode.yml` or point your wrapper directly to a theme file.

## Example: Wrapper (macOS, zsh)
```sh
if (( $+commands[lazygit] )); then
  function lazygit() {
    local LG_THEME
    if [[ $(defaults read -g AppleInterfaceStyle 2>/dev/null) == "Dark" ]]; then
      LG_THEME="${XDG_CONFIG_HOME}/lazygit/themes/modus-vivendi"
    else
      LG_THEME="${XDG_CONFIG_HOME}/lazygit/themes/modus-operandi"
    fi
    command lazygit --use-config-file="${XDG_CONFIG_HOME}/lazygit/config.yml,${LG_THEME}" "$@"
  }
fi
```
