# Glamour Styles

Reusable Glamour JSON styles generated from Modus palettes.

## Render and Validate

```sh
python3 scripts/modus.py render --tool glamour
python3 scripts/modus.py validate --tool glamour
```

Rendered files are written to `ports/glamour/themes/`.

## Consumer Tools

Use consumer-specific commands for install/config.
For Glow, see `ports/glow/README.md` and install with:

```sh
python3 scripts/modus.py install --tool glow
```
