# Glow Themes

Modus themes for [Glow](https://github.com/charmbracelet/glow), generated as Glamour JSON styles.

## Install

Install all themes (symlink mode):

```sh
python3 scripts/modus.py install --tool glow
```

Install one theme:

```sh
python3 scripts/modus.py install --tool glow --theme "modus-operandi"
```

## Activate

Print a ready-to-paste config snippet:

```sh
python3 scripts/modus.py print-config --tool glow --theme modus-vivendi
```

Or set `style` in your `glow.yml` to the installed JSON path, for example:

```yaml
style: "/Users/you/.config/glow/styles/modus-vivendi.json"
```
