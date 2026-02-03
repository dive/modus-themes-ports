# Modus Themes Ports

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3](https://img.shields.io/badge/Python-3-blue.svg)](https://www.python.org/)

Ports of the [Modus themes](https://protesilaos.com/emacs/modus-themes) for terminal tools.

Modus themes are designed by [Protesilaos Stavrou](https://protesilaos.com/about/) with a focus on accessibility—conforming to the highest legibility standard (WCAG AAA). They ship in light/dark variants with tinted and color-deficiency friendly flavors (deuteranopia, tritanopia).

## Supported Tools

| Tool | Description |
|------|-------------|
| [Ghostty](ports/ghostty/README.md) | Terminal emulator |
| [bat](ports/bat/README.md) | Cat clone with syntax highlighting |
| [Lazygit](ports/lazygit/README.md) | Terminal UI for git |
| [LS_COLORS](ports/ls-colors/README.md) | Colors for `ls` and compatible tools |
| [Zed](ports/zed/README.md) | Code editor |
| [Yazi](ports/yazi/README.md) | Terminal file manager |

## Quick Start

```sh
# List available tools and themes
python3 scripts/modus.py list

# Install themes for a tool (creates symlinks)
python3 scripts/modus.py install --tool ghostty

# Install a specific theme
python3 scripts/modus.py install --tool ghostty --theme modus-operandi
```

Themes are symlinked into `$XDG_CONFIG_HOME` by default. See each tool's README for activation instructions.

## Theme Variants

| Variant | Light | Dark |
|---------|-------|------|
| Default | `modus-operandi` | `modus-vivendi` |
| Tinted backgrounds | `modus-operandi-tinted` | `modus-vivendi-tinted` |
| Deuteranopia (red-green) | `modus-operandi-deuteranopia` | `modus-vivendi-deuteranopia` |
| Tritanopia (blue-yellow) | `modus-operandi-tritanopia` | `modus-vivendi-tritanopia` |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) to add new ports—no-code templates supported.

## Credits

All credit for the Modus themes design goes to [Protesilaos Stavrou](https://protesilaos.com/about/). This project ports his work to additional tools.

- Upstream repository: [protesilaos/modus-themes](https://github.com/protesilaos/modus-themes)
- Manual: [Modus Themes Manual](https://protesilaos.com/emacs/modus-themes)

## License

MIT
