# Contributing

Short guide for adding ports and working on the project.

## Quick Start (New Port)

```sh
# 1. Create port structure
mkdir -p ports/mytool

# 2. Add a manifest and template
#    See "Add a New Port" below for details

# 3. Render and validate
python3 scripts/modus.py render --tool mytool
python3 scripts/modus.py validate --tool mytool

# 4. Test install locally
python3 scripts/modus.py install --tool mytool --link
```

## Requirements
- `python3`
- `git`
- `emacs` only for upstream synchronization (system or `python3 scripts/modus.py fetch-emacs` on macOS)

## Core Commands
- Synchronize upstream + regenerate palettes + render themes:
  - `python3 scripts/modus.py sync-upstream`
  - Port-specific palette choices live directly in each tool template; extracted palettes remain unmodified CC0 data.
  - Regenerate hue previews with `python3 scripts/render-hue-previews.py`.
- Render themes:
  - `python3 scripts/modus.py render --tool <tool>`
- Validate themes:
  - `python3 scripts/modus.py validate --tool <tool>`
- Environment check:
  - `python3 scripts/modus.py doctor`
  - Validates: dependencies, palettes, licensing boundaries, generated notices, template tokens, WCAG contrast

## Registry Overview
Tools are discovered from `ports/*/*-port.json`.

Key fields:
- `tool`: tool name
- `theme_dir_rel`: output directory for rendered themes
- `template_path`: template used to generate the port
- `notice_style`: generated notice format (`hash`, `xml`, or `sidecar`)
- `extra_templates`: extra rendered outputs (e.g., `tmtheme.xml`)
- `required_keys`: used by validation for template ports
- `install_targets`: suggested install locations
- `config_locations`: suggested config locations
- `extra_install_dirs`: additional install sources copied under a subdirectory
- `validate_json`: enable JSON validation for template outputs
- `required_fields`: dot-paths required in JSON outputs (e.g., `themes.0.style`)

## Add a New Port
1. Create folder:
   - `ports/<tool>/`
2. Add a manifest:
   - `ports/<tool>/<tool>-port.json`
3. Add a template:
   - `ports/<tool>/theme.tmpl`
4. Render:
   - `python3 scripts/modus.py render --tool <tool>`

Template tokens:
- `{color:<palette-key>}` inserts a palette color
- `{rgb:<palette-key>}` inserts a palette color as `R;G;B`
- `{rgba:<palette-key>}` inserts a palette color as `r g b a` (0-1 floats)
- `{meta:theme}` inserts the palette name
- `{meta:theme_title}` inserts a title-cased theme name
- `{meta:appearance}` inserts `light`/`dark` based on the theme name

Terminal palettes:
- For ANSI 0–15 slots, map to `fg-term-*` and `fg-term-*-bright` (avoid UI colors like `bg-dim`/`fg-dim`).

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

## Licensing Generated Ports

- Keep extracted Modus palette data under CC0-1.0.
- Keep project-authored templates, scripts, and rendered ports under MIT.
- Express palette choices directly in each tool template; do not import upstream Emacs presets.
- Select the appropriate generated notice style in the port manifest; do not duplicate notices in templates.
- Include `ports/NOTICE` and `LICENSES/MIT.txt` when distributing formats that cannot carry comments or license metadata.
