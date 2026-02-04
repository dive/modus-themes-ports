#!/usr/bin/env python3
"""Template rendering for Modus theme ports."""

import re
from typing import Any

TOKEN_RE = re.compile(r"\{(color|value|meta|rgb):([A-Za-z0-9_-]+)\}")


def _theme_title(theme: str) -> str:
    return " ".join([part.capitalize() for part in theme.split("-")])


def _hex_to_rgb(value: str) -> str:
    if not isinstance(value, str) or not value.startswith("#") or len(value) != 7:
        raise ValueError(f"Expected #RRGGBB value, got: {value}")
    r = int(value[1:3], 16)
    g = int(value[3:5], 16)
    b = int(value[5:7], 16)
    return f"{r};{g};{b}"


def _resolve_palette_value(palette: dict[str, str], key: str) -> str:
    """Resolve a palette value, following one level of indirection if needed."""
    value = palette[key]
    if isinstance(value, str) and value in palette:
        return palette[value]
    return value


def render_template(
    template: str,
    palette: dict[str, str],
    mapping: dict[str, Any],
    theme_name: str,
) -> str:
    def replace(match):
        kind, key = match.group(1), match.group(2)
        if kind == "color":
            if key not in palette:
                raise KeyError(f"Missing palette key: {key}")
            value = palette[key]
            if value == "unspecified":
                raise ValueError(
                    f"Palette key '{key}' is unspecified and cannot be used in templates"
                )
            return str(value)
        if kind == "value":
            if key not in mapping:
                raise KeyError(f"Missing mapping key: {key}")
            return str(mapping[key])
        if kind == "rgb":
            if key not in palette:
                raise KeyError(f"Missing palette key: {key}")
            value = _resolve_palette_value(palette, key)
            if value == "unspecified":
                raise ValueError(
                    f"Palette key '{key}' is unspecified and cannot be used in templates"
                )
            return _hex_to_rgb(value)
        if kind == "meta":
            if key == "theme":
                return theme_name
            if key == "theme_title":
                return _theme_title(theme_name)
            if key == "appearance":
                return "light" if theme_name.startswith("modus-operandi") else "dark"
            raise KeyError(f"Unknown meta key: {key}")
        raise KeyError(f"Unknown token kind: {kind}")

    return TOKEN_RE.sub(replace, template)


# Valid meta keys that can be used in templates
_VALID_META_KEYS = {"theme", "theme_title", "appearance"}


def validate_template(
    template: str,
    palette_keys: set[str],
    mapping_keys: set[str],
) -> list[str]:
    """Validate that all template tokens reference valid keys.

    Args:
        template: The template string to validate.
        palette_keys: Set of valid palette key names.
        mapping_keys: Set of valid mapping key names.

    Returns:
        A list of error messages (empty if valid).
    """
    errors: list[str] = []
    seen: set[tuple[str, str]] = set()

    for match in TOKEN_RE.finditer(template):
        kind, key = match.group(1), match.group(2)
        if (kind, key) in seen:
            continue
        seen.add((kind, key))

        if kind == "color" or kind == "rgb":
            if key not in palette_keys:
                errors.append(f"Unknown palette key: {key}")
        elif kind == "value":
            if key not in mapping_keys:
                errors.append(f"Unknown mapping key: {key}")
        elif kind == "meta":
            if key not in _VALID_META_KEYS:
                errors.append(f"Unknown meta key: {key}")

    return errors
