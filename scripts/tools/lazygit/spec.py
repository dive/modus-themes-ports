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


def render(theme_name, palette, mapping) -> str:
    lines = ["gui:", "  theme:"]

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
                value = f"\"{value}\""
            lines.append(f"      - {value}")

    return "\n".join(lines) + "\n"


def validate(text: str):
    found_keys = set()
    in_gui = False
    in_theme = False

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
