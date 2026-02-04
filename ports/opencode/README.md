# OpenCode Modus Themes

## Install
Install all themes (symlink mode):
- `python3 scripts/modus.py install --tool opencode`

Install a single theme:
- `python3 scripts/modus.py install --tool opencode --theme "modus-operandi"`

## Activate
Set the theme in your OpenCode config (e.g. `~/.config/opencode/opencode.json`):
`"theme": "modus-operandi"`

## Notes
Themes are installed under `$XDG_CONFIG_HOME/opencode/themes/`.
OpenCode also loads project themes from `.opencode/themes/`.
The built-in `system` theme follows your terminal’s color scheme (background/foreground). If you prefer that adaptive look, set `"theme": "system"` instead of using the Modus themes.

More info: [OpenCode system theme](https://opencode.ai/docs/themes/#system-theme)

> The `system` theme is designed to automatically adapt to your terminal’s color scheme. Unlike traditional themes that use fixed colors, the system theme:
> - **Generates gray scale**: Creates a custom gray scale based on your terminal’s background color, ensuring optimal contrast.
> - **Uses ANSI colors**: Leverages standard ANSI colors (0-15) for syntax highlighting and UI elements, which respect your terminal’s color palette.
> - **Preserves terminal defaults**: Uses `none` for text and background colors to maintain your terminal’s native appearance.
> 
> The system theme is for users who:
> - Want OpenCode to match their terminal’s appearance
> - Use custom terminal color schemes
> - Prefer a consistent look across all terminal applications
