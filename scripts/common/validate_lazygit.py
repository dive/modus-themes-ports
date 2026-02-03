#!/usr/bin/env python3
import re


def extract_theme_keys(text: str):
    in_gui = False
    in_theme = False
    theme_indent = None
    keys = set()

    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("gui:"):
            in_gui = True
            in_theme = False
            theme_indent = None
            continue
        if in_gui and line.startswith("  theme:"):
            in_theme = True
            theme_indent = None
            continue
        if in_theme:
            if theme_indent is None:
                if line.startswith("    ") and line.strip().endswith(":"):
                    theme_indent = len(line) - len(line.lstrip(" "))
                else:
                    continue
            indent = len(line) - len(line.lstrip(" "))
            if indent < theme_indent:
                in_theme = False
                continue
            if line.strip().endswith(":") and indent == theme_indent:
                key = line.strip().rstrip(":")
                keys.add(key)

    return keys


def validate(text: str, required_keys):
    keys = extract_theme_keys(text)
    missing = sorted(set(required_keys) - keys)
    if missing:
        return [f"Missing keys: {', '.join(missing)}"]
    return []
