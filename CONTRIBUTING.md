# Contributing

Short guide for adding ports and working on the project.

## Requirements
- `python3`
- `git` with `git subtree`
- `emacs` (system) or `python3 scripts/modus.py fetch-emacs` (macOS)

## Core Commands
- Update subtree + regenerate palettes + render themes:
  - `python3 scripts/modus.py update-subtree`
- Extract palettes only:
  - `python3 scripts/modus.py extract-palettes`
- Render themes:
  - `python3 scripts/modus.py render --tool <tool>`
- Validate themes:
  - `python3 scripts/modus.py validate --tool <tool>`
- Environment check:
  - `python3 scripts/modus.py doctor`

## Registry Overview
Tools are discovered from `ports/*/*-port.json`.

Key fields:
- `tool`: tool name
- `theme_dir_rel`: output directory for rendered themes
- `mapping_path`: mapping JSON for the tool
- `template_path`: template file for no-code ports
- `template_format`: currently `mini`
- `required_keys`: used by validation for template ports
- `spec_path`: optional Python spec for advanced ports
- `install_targets`: suggested install locations
- `config_locations`: suggested config locations

## Add a New Port (No-Code)
1. Create folder:
   - `ports/<tool>/`
2. Add manifest:
   - `ports/<tool>/<tool>-port.json`
3. Add mapping:
   - `mappings/<tool>/default.json`
4. Add template:
   - `ports/<tool>/theme.tmpl`
5. Render:
   - `python3 scripts/modus.py render --tool <tool>`

Template tokens:
- `{color:<palette-key>}` inserts a palette color
- `{value:<mapping-key>}` inserts a mapping value

## Add a New Port (Spec-Based)
If templates are insufficient, add:
- `scripts/tools/<tool>/spec.py` implementing:
  - `render(theme_name, palette, mapping) -> str`
  - `validate(text) -> list[str]`
Then add `"spec_path": "scripts/tools/<tool>/spec.py"` to the manifest.

## Naming
All theme filenames are kebab-case with no extension (e.g. `modus-operandi`).

## Config Paths
Use `XDG_CONFIG_HOME` (or `~/.config`). Do not use `~/Library/Application Support`.

## Testing
Recommended checks:
- `python3 scripts/modus.py render --tool all`
- `python3 scripts/modus.py validate --tool all`
