# modus-themes-ports
Modus theme ports for the tools & editors in my workflow

## Requirements
- `git` with `git subtree`
- `emacs` (system) or `python3 scripts/modus.py fetch-emacs` (macOS)
- `python3` (render + validation)

## Quick start
1. Update subtree + generate palettes + render themes:
   - `python3 scripts/modus.py update-subtree`

2. If you do not have Emacs installed:
   - `python3 scripts/modus.py fetch-emacs`

3. Install Ghostty themes:
   - `python3 scripts/modus.py install --tool ghostty`

## Commands
- `python3 scripts/modus.py list`
- `python3 scripts/modus.py render --tool ghostty`
- `python3 scripts/modus.py render --tool lazygit`
- `python3 scripts/modus.py render --tool all`
- `python3 scripts/modus.py validate --tool ghostty`
- `python3 scripts/modus.py validate --tool lazygit`
- `python3 scripts/modus.py validate --tool all`
- `python3 scripts/modus.py doctor`

## Scripts
- `python3 scripts/modus.py update-subtree`: update `vendor/modus-themes`, regenerate palettes, and render themes
- `python3 scripts/modus.py fetch-emacs`: download and cache Emacs.app in `.emacs-app/`
- `python3 scripts/modus.py extract-palettes`: generate `palettes/*.json` from the subtree
- `python3 scripts/modus.py render --tool ghostty`: render `ports/ghostty/themes/*`
- `python3 scripts/modus.py render --tool lazygit`: render `ports/lazygit/themes/*`
- `python3 scripts/modus.py install --tool <tool>`: install themes
- `python3 scripts/modus.py validate --tool ghostty`: validate Ghostty theme files
- `python3 scripts/modus.py validate --tool lazygit`: validate Lazygit theme files
- `python3 scripts/modus.py doctor`: check environment and dependencies

## Naming
All ported theme filenames use kebab-case with no extension (e.g. `modus-operandi`). Use the kebab-case name in tool configs.

## Config paths
All tooling defaults to `XDG_CONFIG_HOME` (or `~/.config`) and does not use `~/Library/Application Support`.
