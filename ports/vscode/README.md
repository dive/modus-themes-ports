# Visual Studio Code Modus Themes

## Install

Install all themes (symlink mode):
- `python3 scripts/modus.py install --tool vscode`

Install a single theme:
- `python3 scripts/modus.py install --tool vscode --theme "modus-operandi"`

Themes and the extension manifest are installed to:
- `~/.vscode/extensions/modus-themes/`

Visual Studio Code discovers extensions in that directory automatically on next launch.

If Visual Studio Code does not pick up symlinked themes, install with copy mode:
- `python3 scripts/modus.py install --tool vscode --copy`

## Activate

1. Open Visual Studio Code.
2. Go to `Code → Preferences → Color Theme` (or press `⌘K ⌘T`).
3. Select a `Modus *` theme.

## Uninstall

- `python3 scripts/modus.py uninstall --tool vscode`
