# modus-themes-ports

Ports of the Modus themes for terminal tools.

Modus themes are by [Protesilaos Stavrou](https://protesilaos.com/about/). They prioritize accessibility and high contrast, conforming to the WCAG AAA standard, with light/dark variants and additional variants such as tinted and color-deficiency friendly themes. For details, see the upstream repository and manual: `https://github.com/protesilaos/modus-themes` and `https://protesilaos.com/emacs/modus-themes`.

## Requirements
- `python3`

## Supported Ports
- [Ghostty](ports/ghostty/README.md)
- [Lazygit](ports/lazygit/README.md)

## Install
- `python3 scripts/modus.py install --tool <tool>`
- `python3 scripts/modus.py list`

By default, install symlinks themes into `$XDG_CONFIG_HOME/<tool>/themes`.
See each tool README for how to activate a theme.

## Contributing
See `CONTRIBUTING.md` to add new ports (no-code templates supported).

## License
See `LICENSE`.
