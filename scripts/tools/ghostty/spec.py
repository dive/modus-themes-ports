import re

REQUIRED_KEYS = {
    "background",
    "foreground",
    "cursor-color",
    "selection-background",
    "selection-foreground",
}


def render(theme_name, palette, mapping) -> str:
    required_map_keys = [
        "background",
        "foreground",
        "cursor-color",
        "selection-background",
        "selection-foreground",
        "palette",
    ]
    for key in required_map_keys:
        if key not in mapping:
            raise KeyError(f"Missing mapping key: {key}")

    def resolve(palette_key: str) -> str:
        if palette_key not in palette:
            raise KeyError(f"Missing palette key: {palette_key}")
        return palette[palette_key]

    lines = []
    for key in required_map_keys[:-1]:
        palette_key = mapping[key]
        color = resolve(palette_key)
        lines.append(f"{key} = {color}")

    palette_map = mapping["palette"]
    for i in range(16):
        idx = str(i)
        if idx not in palette_map:
            raise KeyError(f"Missing palette mapping for index {idx}")
        color = resolve(palette_map[idx])
        lines.append(f"palette = {i}={color}")

    return "\n".join(lines) + "\n"


def validate(text: str):
    lines = [line.strip() for line in text.splitlines()]
    found_keys = set()
    palette_indices = set()

    palette_re = re.compile(r"^palette\s*=\s*(\d+)\s*=\s*(#[0-9A-Fa-f]{6,8})$")
    key_re = re.compile(r"^([a-zA-Z-]+)\s*=\s*(#[0-9A-Fa-f]{6,8})$")

    for line in lines:
        if not line or line.startswith("#"):
            continue
        m = palette_re.match(line)
        if m:
            palette_indices.add(int(m.group(1)))
            continue
        m = key_re.match(line)
        if m:
            found_keys.add(m.group(1))

    errors = []
    missing_keys = REQUIRED_KEYS - found_keys
    if missing_keys:
        errors.append(f"Missing keys: {', '.join(sorted(missing_keys))}")

    missing_palette = [str(i) for i in range(16) if i not in palette_indices]
    if missing_palette:
        errors.append(f"Missing palette indices: {', '.join(missing_palette)}")

    return errors
