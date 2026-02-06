# Contributing

Short guide for adding ports and working on the project.

## Quick Start (New Port)

```sh
# 1. Create port structure
mkdir -p ports/mytool mappings/mytool

# 2. Add manifest, mapping, and template
#    See "Add a New Port (No-Code)" below for details

# 3. Render and validate
python3 scripts/modus.py render --tool mytool
python3 scripts/modus.py validate --tool mytool

# 4. Test install locally
python3 scripts/modus.py install --tool mytool --link
```

## Requirements
- `python3`
- `git` with `git subtree`
- `emacs` (system) or `python3 scripts/modus.py fetch-emacs` (macOS)

## Core Commands
- Update subtree + regenerate palettes + render themes:
  - `python3 scripts/modus.py update-subtree`
- Extract palettes only:
  - `python3 scripts/modus.py extract-palettes`
  - Note: palette extraction applies the Modus faint preset.
  - Regenerate hue previews with `python3 scripts/render-hue-previews.py`.
- Render themes:
  - `python3 scripts/modus.py render --tool <tool>`
- Validate themes:
  - `python3 scripts/modus.py validate --tool <tool>`
- Environment check:
  - `python3 scripts/modus.py doctor`
  - Validates: dependencies, palettes, template tokens, WCAG contrast

## Registry Overview
Tools are discovered from `ports/*/*-port.json`.

Key fields:
- `tool`: tool name
- `theme_dir_rel`: output directory for rendered themes
- `mapping_path`: mapping JSON for the tool
- `template_path`: template file for no-code ports
- `template_format`: currently `mini`
- `extra_templates`: extra rendered outputs (e.g., `tmtheme.xml`)
- `required_keys`: used by validation for template ports
- `spec_path`: optional Python spec for advanced ports
- `install_targets`: suggested install locations
- `config_locations`: suggested config locations
- `extra_install_dirs`: additional install sources copied under a subdirectory
- `validate_json`: enable JSON validation for template outputs
- `required_fields`: dot-paths required in JSON outputs (e.g., `themes.0.style`)

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
- `{rgb:<palette-key>}` inserts a palette color as `R;G;B`
- `{rgba:<palette-key>}` inserts a palette color as `r g b a` (0-1 floats)
- `{meta:theme}` inserts the palette name
- `{meta:theme_title}` inserts a title-cased theme name
- `{meta:appearance}` inserts `light`/`dark` based on the theme name

Terminal palettes:
- For ANSI 0–15 slots, map to `fg-term-*` and `fg-term-*-bright` (avoid UI colors like `bg-dim`/`fg-dim`).

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

## Accessibility

Modus themes are designed to meet WCAG AAA (7:1 contrast ratio). The `doctor` command checks contrast for all palette colors. Warnings for tinted variants may be intentional design choices.

Key foreground colors to check against `bg-main`:
- `fg-main`, `fg-dim`, `fg-alt`
- Named colors: `red`, `green`, `blue`, `yellow`, `magenta`, `cyan`
- Variants: `*-warmer`, `*-cooler`, `*-faint`

## Testing

Recommended checks:
- `python3 scripts/modus.py render --tool all`
- `python3 scripts/modus.py validate --tool all`
- `python3 scripts/modus.py doctor`
