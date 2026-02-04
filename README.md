# Modus Themes Ports

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3](https://img.shields.io/badge/Python-3-blue.svg)](https://www.python.org/)

Ports of the [Modus themes](https://protesilaos.com/emacs/modus-themes) for terminal tools.

Modus themes are designed by [Protesilaos Stavrou](https://protesilaos.com/about/) with a focus on accessibility—conforming to the highest legibility standard (WCAG AAA). They ship in light/dark variants with tinted and color-deficiency friendly flavors (deuteranopia, tritanopia).

## Supported Tools

| Tool | Description |
|------|-------------|
| [Amp](ports/amp/README.md) | AI coding agent CLI |
| [Ghostty](ports/ghostty/README.md) | Terminal emulator |
| [Helix](ports/helix/README.md) | Modal text editor |
| [bat](ports/bat/README.md) | Cat clone with syntax highlighting |
| [Lazygit](ports/lazygit/README.md) | Terminal UI for git |
| [LS_COLORS](ports/ls-colors/README.md) | Colors for `ls` and compatible tools |
| [OpenCode](ports/opencode/README.md) | AI coding agent CLI |
| [Pi](ports/pi/README.md) | AI coding agent CLI |
| [Zed](ports/zed/README.md) | Code editor |
| [Yazi](ports/yazi/README.md) | Terminal file manager |

Screenshots: [SCREENSHOTS.md](SCREENSHOTS.md)

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

## Accent Hue Reference

Preview of the core accent foreground hues by variant (base, warmer, cooler, faint, intense).
Docs: https://protesilaos.com/emacs/modus-themes

### modus-operandi
| Hue | base | warmer | cooler | faint | intense |
|---|---|---|---|---|---|
| red | `#a60000` <span style="display:inline-block;width:0.8em;height:0.8em;background:#a60000;border:1px solid #000;vertical-align:middle;"></span> | `#972500` <span style="display:inline-block;width:0.8em;height:0.8em;background:#972500;border:1px solid #000;vertical-align:middle;"></span> | `#a0132f` <span style="display:inline-block;width:0.8em;height:0.8em;background:#a0132f;border:1px solid #000;vertical-align:middle;"></span> | `#7f0000` <span style="display:inline-block;width:0.8em;height:0.8em;background:#7f0000;border:1px solid #000;vertical-align:middle;"></span> | `#d00000` <span style="display:inline-block;width:0.8em;height:0.8em;background:#d00000;border:1px solid #000;vertical-align:middle;"></span> |
| green | `#006800` <span style="display:inline-block;width:0.8em;height:0.8em;background:#006800;border:1px solid #000;vertical-align:middle;"></span> | `#316500` <span style="display:inline-block;width:0.8em;height:0.8em;background:#316500;border:1px solid #000;vertical-align:middle;"></span> | `#00663f` <span style="display:inline-block;width:0.8em;height:0.8em;background:#00663f;border:1px solid #000;vertical-align:middle;"></span> | `#2a5045` <span style="display:inline-block;width:0.8em;height:0.8em;background:#2a5045;border:1px solid #000;vertical-align:middle;"></span> | `#008900` <span style="display:inline-block;width:0.8em;height:0.8em;background:#008900;border:1px solid #000;vertical-align:middle;"></span> |
| yellow | `#6f5500` <span style="display:inline-block;width:0.8em;height:0.8em;background:#6f5500;border:1px solid #000;vertical-align:middle;"></span> | `#884900` <span style="display:inline-block;width:0.8em;height:0.8em;background:#884900;border:1px solid #000;vertical-align:middle;"></span> | `#7a4f2f` <span style="display:inline-block;width:0.8em;height:0.8em;background:#7a4f2f;border:1px solid #000;vertical-align:middle;"></span> | `#624416` <span style="display:inline-block;width:0.8em;height:0.8em;background:#624416;border:1px solid #000;vertical-align:middle;"></span> | `#808000` <span style="display:inline-block;width:0.8em;height:0.8em;background:#808000;border:1px solid #000;vertical-align:middle;"></span> |
| blue | `#0031a9` <span style="display:inline-block;width:0.8em;height:0.8em;background:#0031a9;border:1px solid #000;vertical-align:middle;"></span> | `#3548cf` <span style="display:inline-block;width:0.8em;height:0.8em;background:#3548cf;border:1px solid #000;vertical-align:middle;"></span> | `#0000b0` <span style="display:inline-block;width:0.8em;height:0.8em;background:#0000b0;border:1px solid #000;vertical-align:middle;"></span> | `#003497` <span style="display:inline-block;width:0.8em;height:0.8em;background:#003497;border:1px solid #000;vertical-align:middle;"></span> | `#0000ff` <span style="display:inline-block;width:0.8em;height:0.8em;background:#0000ff;border:1px solid #000;vertical-align:middle;"></span> |
| magenta | `#721045` <span style="display:inline-block;width:0.8em;height:0.8em;background:#721045;border:1px solid #000;vertical-align:middle;"></span> | `#8f0075` <span style="display:inline-block;width:0.8em;height:0.8em;background:#8f0075;border:1px solid #000;vertical-align:middle;"></span> | `#531ab6` <span style="display:inline-block;width:0.8em;height:0.8em;background:#531ab6;border:1px solid #000;vertical-align:middle;"></span> | `#7c318f` <span style="display:inline-block;width:0.8em;height:0.8em;background:#7c318f;border:1px solid #000;vertical-align:middle;"></span> | `#dd22dd` <span style="display:inline-block;width:0.8em;height:0.8em;background:#dd22dd;border:1px solid #000;vertical-align:middle;"></span> |
| cyan | `#005e8b` <span style="display:inline-block;width:0.8em;height:0.8em;background:#005e8b;border:1px solid #000;vertical-align:middle;"></span> | `#3f578f` <span style="display:inline-block;width:0.8em;height:0.8em;background:#3f578f;border:1px solid #000;vertical-align:middle;"></span> | `#005f5f` <span style="display:inline-block;width:0.8em;height:0.8em;background:#005f5f;border:1px solid #000;vertical-align:middle;"></span> | `#005077` <span style="display:inline-block;width:0.8em;height:0.8em;background:#005077;border:1px solid #000;vertical-align:middle;"></span> | `#008899` <span style="display:inline-block;width:0.8em;height:0.8em;background:#008899;border:1px solid #000;vertical-align:middle;"></span> |

### modus-vivendi
| Hue | base | warmer | cooler | faint | intense |
|---|---|---|---|---|---|
| red | `#ff5f59` <span style="display:inline-block;width:0.8em;height:0.8em;background:#ff5f59;border:1px solid #000;vertical-align:middle;"></span> | `#ff6b55` <span style="display:inline-block;width:0.8em;height:0.8em;background:#ff6b55;border:1px solid #000;vertical-align:middle;"></span> | `#ff7f86` <span style="display:inline-block;width:0.8em;height:0.8em;background:#ff7f86;border:1px solid #000;vertical-align:middle;"></span> | `#ff9580` <span style="display:inline-block;width:0.8em;height:0.8em;background:#ff9580;border:1px solid #000;vertical-align:middle;"></span> | `#ff5f5f` <span style="display:inline-block;width:0.8em;height:0.8em;background:#ff5f5f;border:1px solid #000;vertical-align:middle;"></span> |
| green | `#44bc44` <span style="display:inline-block;width:0.8em;height:0.8em;background:#44bc44;border:1px solid #000;vertical-align:middle;"></span> | `#70b900` <span style="display:inline-block;width:0.8em;height:0.8em;background:#70b900;border:1px solid #000;vertical-align:middle;"></span> | `#00c06f` <span style="display:inline-block;width:0.8em;height:0.8em;background:#00c06f;border:1px solid #000;vertical-align:middle;"></span> | `#88ca9f` <span style="display:inline-block;width:0.8em;height:0.8em;background:#88ca9f;border:1px solid #000;vertical-align:middle;"></span> | `#44df44` <span style="display:inline-block;width:0.8em;height:0.8em;background:#44df44;border:1px solid #000;vertical-align:middle;"></span> |
| yellow | `#d0bc00` <span style="display:inline-block;width:0.8em;height:0.8em;background:#d0bc00;border:1px solid #000;vertical-align:middle;"></span> | `#fec43f` <span style="display:inline-block;width:0.8em;height:0.8em;background:#fec43f;border:1px solid #000;vertical-align:middle;"></span> | `#dfaf7a` <span style="display:inline-block;width:0.8em;height:0.8em;background:#dfaf7a;border:1px solid #000;vertical-align:middle;"></span> | `#d2b580` <span style="display:inline-block;width:0.8em;height:0.8em;background:#d2b580;border:1px solid #000;vertical-align:middle;"></span> | `#efef00` <span style="display:inline-block;width:0.8em;height:0.8em;background:#efef00;border:1px solid #000;vertical-align:middle;"></span> |
| blue | `#2fafff` <span style="display:inline-block;width:0.8em;height:0.8em;background:#2fafff;border:1px solid #000;vertical-align:middle;"></span> | `#79a8ff` <span style="display:inline-block;width:0.8em;height:0.8em;background:#79a8ff;border:1px solid #000;vertical-align:middle;"></span> | `#00bcff` <span style="display:inline-block;width:0.8em;height:0.8em;background:#00bcff;border:1px solid #000;vertical-align:middle;"></span> | `#82b0ec` <span style="display:inline-block;width:0.8em;height:0.8em;background:#82b0ec;border:1px solid #000;vertical-align:middle;"></span> | `#338fff` <span style="display:inline-block;width:0.8em;height:0.8em;background:#338fff;border:1px solid #000;vertical-align:middle;"></span> |
| magenta | `#feacd0` <span style="display:inline-block;width:0.8em;height:0.8em;background:#feacd0;border:1px solid #000;vertical-align:middle;"></span> | `#f78fe7` <span style="display:inline-block;width:0.8em;height:0.8em;background:#f78fe7;border:1px solid #000;vertical-align:middle;"></span> | `#b6a0ff` <span style="display:inline-block;width:0.8em;height:0.8em;background:#b6a0ff;border:1px solid #000;vertical-align:middle;"></span> | `#caa6df` <span style="display:inline-block;width:0.8em;height:0.8em;background:#caa6df;border:1px solid #000;vertical-align:middle;"></span> | `#ff66ff` <span style="display:inline-block;width:0.8em;height:0.8em;background:#ff66ff;border:1px solid #000;vertical-align:middle;"></span> |
| cyan | `#00d3d0` <span style="display:inline-block;width:0.8em;height:0.8em;background:#00d3d0;border:1px solid #000;vertical-align:middle;"></span> | `#4ae2f0` <span style="display:inline-block;width:0.8em;height:0.8em;background:#4ae2f0;border:1px solid #000;vertical-align:middle;"></span> | `#6ae4b9` <span style="display:inline-block;width:0.8em;height:0.8em;background:#6ae4b9;border:1px solid #000;vertical-align:middle;"></span> | `#9ac8e0` <span style="display:inline-block;width:0.8em;height:0.8em;background:#9ac8e0;border:1px solid #000;vertical-align:middle;"></span> | `#00eff0` <span style="display:inline-block;width:0.8em;height:0.8em;background:#00eff0;border:1px solid #000;vertical-align:middle;"></span> |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) to add new ports—no-code templates supported.

## Credits

All credit for the Modus themes design goes to [Protesilaos Stavrou](https://protesilaos.com/about/). This project ports his work to additional tools.

- Upstream repository: [protesilaos/modus-themes](https://github.com/protesilaos/modus-themes)
- Manual: [Modus Themes Manual](https://protesilaos.com/emacs/modus-themes)

## License

MIT
