# Visual Studio Code Modus Themes

## Install

Install all themes (symlink mode):
- `python3 scripts/modus.py install --tool vscode`

The complete extension—including all themes, package metadata, license, and
notice—is installed atomically to:
- `~/.vscode/extensions/modus-themes/`

Visual Studio Code discovers extensions in that directory automatically on next launch.

If Visual Studio Code does not pick up symlinked themes, install with copy mode:
- `python3 scripts/modus.py install --tool vscode --copy`

Selective `--theme` installation is not supported because a VS Code extension
is one package.

## Activate

1. Open Visual Studio Code.
2. Go to `Code → Preferences → Color Theme` (or press `⌘K ⌘T`).
3. Select a `Modus *` theme.

## Uninstall

- `python3 scripts/modus.py uninstall --tool vscode`
