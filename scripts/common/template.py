#!/usr/bin/env python3
import re

TOKEN_RE = re.compile(r"\{(color|value):([A-Za-z0-9_-]+)\}")


def render_template(template: str, palette: dict, mapping: dict) -> str:
    def replace(match):
        kind, key = match.group(1), match.group(2)
        if kind == "color":
            if key not in palette:
                raise KeyError(f"Missing palette key: {key}")
            return str(palette[key])
        if kind == "value":
            if key not in mapping:
                raise KeyError(f"Missing mapping key: {key}")
            return str(mapping[key])
        raise KeyError(f"Unknown token kind: {kind}")

    return TOKEN_RE.sub(replace, template)
