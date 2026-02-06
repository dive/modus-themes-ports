# Xcode Modus Themes

## Install
Install all themes:
- `python3 scripts/modus.py install --tool xcode`

Install a single theme:
- `python3 scripts/modus.py install --tool xcode --theme "modus-operandi"`

Themes are installed to:
- `~/Library/Developer/Xcode/UserData/FontAndColorThemes/`

If Xcode does not pick up symlinked themes immediately, install with:
- `python3 scripts/modus.py install --tool xcode --copy`

## Activate
1. Open Xcode.
2. Go to `Xcode -> Settings -> Themes`.
3. Select a `modus-*` theme.

## Uninstall
- `python3 scripts/modus.py uninstall --tool xcode`
