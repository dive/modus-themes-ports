# Amp Themes

Modus Themes for the [Amp](https://ampcode.com) CLI.

## Installation

Copy the theme directories to `~/.config/amp/themes/`:

```sh
python3 scripts/modus.py install --tool amp
```

Or use symbolic links:

```sh
python3 scripts/modus.py install --tool amp --link
```

## Usage

Switch themes using the command palette (`Ctrl+O`) and selecting `theme: switch`.

Or set in `~/.config/amp/settings.json`:

```json
{
  "amp.terminal.theme": "modus-vivendi"
}
```

> [!NOTE]
> Amp doesn't support automatic dark/light theme switching based on system appearance.
> You'll need to manually switch themes via the command palette or by changing settings.

Available themes:
- `modus-operandi` — light theme
- `modus-operandi-tinted` — light theme with subtle tinted backgrounds
- `modus-operandi-deuteranopia` — light theme optimized for red-green color deficiency
- `modus-operandi-tritanopia` — light theme optimized for blue-yellow color deficiency
- `modus-vivendi` — dark theme
- `modus-vivendi-tinted` — dark theme with subtle tinted backgrounds
- `modus-vivendi-deuteranopia` — dark theme optimized for red-green color deficiency
- `modus-vivendi-tritanopia` — dark theme optimized for blue-yellow color deficiency

## Uninstall

```sh
python3 scripts/modus.py uninstall --tool amp
```
