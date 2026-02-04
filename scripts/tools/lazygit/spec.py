"""Lazygit theme spec for Modus theme ports."""

from __future__ import annotations

from typing import Any

REQUIRED_KEYS = {
    "activeBorderColor",
    "inactiveBorderColor",
    "searchingActiveBorderColor",
    "optionsTextColor",
    "selectedLineBgColor",
    "inactiveViewSelectedLineBgColor",
    "cherryPickedCommitFgColor",
    "cherryPickedCommitBgColor",
    "markedBaseCommitFgColor",
    "markedBaseCommitBgColor",
    "unstagedChangesColor",
    "defaultFgColor",
}

ORDER = [
    "activeBorderColor",
    "inactiveBorderColor",
    "searchingActiveBorderColor",
    "optionsTextColor",
    "selectedLineBgColor",
    "inactiveViewSelectedLineBgColor",
    "cherryPickedCommitFgColor",
    "cherryPickedCommitBgColor",
    "markedBaseCommitFgColor",
    "markedBaseCommitBgColor",
    "unstagedChangesColor",
    "defaultFgColor",
]


def render(
    theme_name: str,
    palette: dict[str, str],
    mapping: dict[str, Any],
) -> str:
    """Render a Lazygit theme configuration.

    Args:
        theme_name: Name of the theme (unused but required by spec interface).
        palette: Resolved palette dictionary.
        mapping: Mapping configuration with color assignments.

    Returns:
        Rendered Lazygit theme YAML content.
    """
    if "authorColor" not in mapping:
        raise KeyError("Missing mapping key: authorColor")

    author_token = mapping["authorColor"]
    author_value = palette.get(author_token, author_token)
    if isinstance(author_value, str) and author_value.startswith("#"):
        author_value = f'"{author_value}"'

    lines: list[str] = [
        "gui:",
        "  authorColors:",
        f"    '*': {author_value}",
        "  theme:",
    ]

    for key in ORDER:
        if key not in mapping:
            raise KeyError(f"Missing mapping key: {key}")
        tokens = mapping[key]
        if not isinstance(tokens, list):
            raise TypeError(f"Mapping for {key} must be a list")
        lines.append(f"    {key}:")
        for token in tokens:
            value = palette.get(token, token)
            if isinstance(value, str) and value.startswith("#"):
                value = f'"{value}"'
            lines.append(f"      - {value}")

    return "\n".join(lines) + "\n"


def validate(text: str) -> list[str]:
    """Validate a Lazygit theme configuration.

    Args:
        text: Theme file content.

    Returns:
        List of validation error messages (empty if valid).
    """
    found_keys: set[str] = set()
    in_gui = False
    in_theme = False

    if "authorColors:" not in text or "'*':" not in text:
        return ["Missing authorColors"]

    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("gui:"):
            in_gui = True
            in_theme = False
            continue
        if in_gui and line.startswith("  theme:"):
            in_theme = True
            continue
        if in_theme and line.startswith("    ") and line.strip().endswith(":"):
            key = line.strip().rstrip(":")
            found_keys.add(key)

    missing = REQUIRED_KEYS - found_keys
    if missing:
        return [f"Missing keys: {', '.join(sorted(missing))}"]

    return []
