# modus-themes-ports

Ports of the Modus themes for terminal tools.

Modus themes are by [Protesilaos Stavrou](https://protesilaos.com/about/). They prioritize accessibility and high contrast, conforming to WCAG AAA, and ship in light/dark variants with tinted and color-deficiency friendly flavors (deuteranopia, tritanopia). For details, see the upstream repository and manual: `https://github.com/protesilaos/modus-themes` and `https://protesilaos.com/emacs/modus-themes`.

## Supported Ports
- [Ghostty](ports/ghostty/README.md)
- [bat](ports/bat/README.md)
- [Lazygit](ports/lazygit/README.md)
- [LS_COLORS](ports/ls-colors/README.md)
- [Yazi](ports/yazi/README.md)

## How It Works
Themes are generated from the original Emacs Modus palettes and rendered into tool-specific formats (a bit overengineered, but it works).

## Requirements
- `python3`

## Install
- `python3 scripts/modus.py install --tool <tool>`
- `python3 scripts/modus.py list`

By default, install symlinked themes into `$XDG_CONFIG_HOME` (see each tool README for the exact path).
See each tool README for how to activate a theme.

## Contributing
See `CONTRIBUTING.md` to add new ports (no-code templates supported).
