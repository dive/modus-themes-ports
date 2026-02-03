# Contributing

Thanks for your interest in contributing a new port.

## Quick Start: No-Code Port
You can add a new tool without writing Python by using a template and a manifest.

### 1) Create a port folder
```
ports/<tool>/
```

### 2) Add a manifest
Create `ports/<tool>/<tool>-port.json`:
```
{
  "tool": "<tool>",
  "theme_dir_rel": "ports/<tool>/themes",
  "theme_ext": "",
  "mapping_path": "mappings/<tool>/default.json",
  "template_path": "ports/<tool>/theme.tmpl",
  "template_format": "mini",
  "required_keys": ["..."],
  "install_targets": ["$XDG_CONFIG_HOME/<tool>/themes", "$HOME/.config/<tool>/themes"],
  "config_locations": ["$XDG_CONFIG_HOME/<tool>/config", "$HOME/.config/<tool>/config"]
}
```

### 3) Add a mapping
Create `mappings/<tool>/default.json` with palette key references (e.g. `bg-main`, `fg-main`).

### 4) Add a template
Create `ports/<tool>/theme.tmpl` and use the mini template syntax:
- `{color:<palette-key>}` inserts a palette color
- `{value:<mapping-key>}` inserts a mapping value

### 5) Render
```
python3 scripts/modus.py render --tool <tool>
```

## Advanced: Spec-Based Port
If templates are too limited, provide a Python spec:
- `scripts/tools/<tool>/spec.py` implements:
  - `render(theme_name, palette, mapping) -> str`
  - `validate(text) -> list[str]`

Then add `"spec_path": "scripts/tools/<tool>/spec.py"` in the manifest.

## Notes
- Filenames must be kebab-case with no extension.
- Use `XDG_CONFIG_HOME` for config paths.
