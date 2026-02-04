#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

HUES = ["red", "green", "yellow", "blue", "magenta", "cyan"]
VARIANTS = [("base", ""), ("warmer", "-warmer"), ("cooler", "-cooler"), ("faint", "-faint"), ("intense", "-intense")]
HEADERS = ["Hue"] + [label for label, _ in VARIANTS]

START_X = 20
START_Y = 50
TITLE_Y = 28
COL_WIDTH = 130
HEADER_HEIGHT = 36
ROW_HEIGHT = 36
SWATCH_SIZE = 12


def make_svg(theme_name: str, palette: dict[str, str]) -> str:
    cols = len(HEADERS)
    rows = len(HUES)
    width = START_X * 2 + COL_WIDTH * cols
    table_height = HEADER_HEIGHT + ROW_HEIGHT * rows
    height = START_Y + table_height + 20

    bg_main = palette.get("bg-main", "#ffffff")
    bg_dim = palette.get("bg-dim", "#f6f8fa")
    bg_header = palette.get("bg-active", bg_dim)
    border = palette.get("border", "#d0d7de")
    text_main = palette.get("fg-main", "#111111")

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect width="100%" height="100%" fill="{bg_main}"/>',
        f'<text x="{START_X}" y="{TITLE_Y}" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" '
        f'font-size="22" font-weight="700" fill="{text_main}">{theme_name}</text>',
    ]

    # Header row
    for col, label in enumerate(HEADERS):
        x = START_X + col * COL_WIDTH
        y = START_Y
        lines.append(f'<rect x="{x}" y="{y}" width="{COL_WIDTH}" height="{HEADER_HEIGHT}" fill="{bg_header}" stroke="{border}"/>')
        lines.append(
            f'<text x="{x + COL_WIDTH/2}" y="{y + HEADER_HEIGHT/2}" '
            'font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" '
            f'font-size="14" font-weight="600" fill="{text_main}" dominant-baseline="middle" text-anchor="middle">'
            f'{label}</text>'
        )

    # Data rows
    for row, hue in enumerate(HUES):
        y = START_Y + HEADER_HEIGHT + row * ROW_HEIGHT
        fill = bg_main if row % 2 == 0 else bg_dim
        for col in range(cols):
            x = START_X + col * COL_WIDTH
            lines.append(f'<rect x="{x}" y="{y}" width="{COL_WIDTH}" height="{ROW_HEIGHT}" fill="{fill}" stroke="{border}"/>')
            if col == 0:
                lines.append(
                    f'<text x="{x + 12}" y="{y + ROW_HEIGHT/2}" '
                    'font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" '
                    f'font-size="14" fill="{text_main}" dominant-baseline="middle">'
                    f'{hue}</text>'
                )
            else:
                variant = VARIANTS[col - 1][1]
                key = hue + variant
                value = palette.get(key, "")
                swatch_x = x + 10
                swatch_y = y + (ROW_HEIGHT - SWATCH_SIZE) / 2
                if value:
                    lines.append(
                        f'<rect x="{swatch_x}" y="{swatch_y}" width="{SWATCH_SIZE}" height="{SWATCH_SIZE}" '
                        f'fill="{value}" stroke="{border}"/>'
                    )
                    lines.append(
                        f'<text x="{x + 28}" y="{y + ROW_HEIGHT/2}" '
                        'font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" '
                        f'font-size="13" fill="{value}" dominant-baseline="middle">'
                        f'{value}</text>'
                    )
    lines.append('</svg>')
    return "\n".join(lines)


def main() -> None:
    output_dir = Path("screenshots/hues")
    output_dir.mkdir(parents=True, exist_ok=True)

    for theme in ["modus-operandi", "modus-vivendi"]:
        palette = json.loads(Path(f"palettes/{theme}.json").read_text())['palette']
        svg = make_svg(theme, palette)
        (output_dir / f"{theme}.svg").write_text(svg, encoding="utf-8")
        print(f"Wrote {output_dir / (theme + '.svg')}")


if __name__ == "__main__":
    main()
