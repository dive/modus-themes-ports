#!/usr/bin/env python3
import re

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


def _resolve_palette_value(palette: dict, key: str):
    value = palette[key]
    if isinstance(value, str) and value in palette:
        return palette[value]
    return value


def render_template(template: str, palette: dict, mapping: dict, theme_name: str) -> str:
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
