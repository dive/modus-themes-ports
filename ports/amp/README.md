# Amp Themes

Modus Themes for the [Amp](https://ampcode.com) CLI.

## Installation

Install all themes using symbolic links:

```sh
python3 scripts/modus.py install --tool amp
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

See the repository's [theme variant table](../../README.md#theme-variants) for the complete list of light, dark, tinted, and color-deficiency variants.

## Uninstall

```sh
python3 scripts/modus.py uninstall --tool amp
```
