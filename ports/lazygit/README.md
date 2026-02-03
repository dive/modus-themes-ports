# Lazygit Modus Themes

## Update Flow
1. Update subtree and regenerate palettes + themes:
   - `python3 scripts/modus.py update-subtree`

2. If Emacs is not installed, download it once:
   - `python3 scripts/modus.py fetch-emacs`

3. Manually regenerate palettes:
   - `python3 scripts/modus.py extract-palettes`

4. Render Lazygit themes:
   - `python3 scripts/modus.py render --tool lazygit`

Render all tools:
- `python3 scripts/modus.py render --tool all`

## Install
Install all themes (symlink mode):
- `python3 scripts/modus.py install --tool lazygit`

Install a single theme:
- `python3 scripts/modus.py install --tool lazygit --theme "modus-operandi"`

Print the config block:
- `python3 scripts/modus.py print-config --tool lazygit --theme "modus-operandi"`

## Config override
Lazygit does not automatically load per-theme files. You must explicitly pass config paths via `--use-config-file`.

Docs:
- `https://github.com/jesseduffield/lazygit/blob/master/docs/Config.md#overriding-default-config-file-location`

Themes are installed under `$XDG_CONFIG_HOME/lazygit/themes/`. You can symlink one to `light-mode.yml`/`dark-mode.yml` or point your wrapper directly to a theme file.

## Example: Wrapper
Zsh example for `.zshrc` on macOS. Uses system appearance (light/dark) to select a theme and combines it with your main config.

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

## Uninstall
Remove installed symlinks:
- `python3 scripts/modus.py uninstall --tool lazygit`

## Config paths
Uses `XDG_CONFIG_HOME` (or `~/.config`) only.

## Naming
All ports use kebab-case filenames with no extension (e.g. `modus-operandi`).
