#!/usr/bin/env python3
"""WCAG contrast ratio utilities for Modus theme ports.

Modus themes are designed to meet WCAG AAA standards, requiring a
minimum contrast ratio of 7:1 for normal text.
"""

from __future__ import annotations


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert a hex color string to RGB tuple.

    Args:
        hex_color: Color in #RRGGBB format.

    Returns:
        Tuple of (red, green, blue) values 0-255.
    """
    if not hex_color.startswith("#") or len(hex_color) != 7:
        raise ValueError(f"Expected #RRGGBB format, got: {hex_color}")
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    return r, g, b


def relative_luminance(hex_color: str) -> float:
    """Calculate relative luminance per WCAG 2.1.

    See: https://www.w3.org/TR/WCAG21/#dfn-relative-luminance

    Args:
        hex_color: Color in #RRGGBB format.

    Returns:
        Relative luminance value between 0 and 1.
    """
    r, g, b = hex_to_rgb(hex_color)

    def channel_luminance(value: int) -> float:
        srgb = value / 255
        if srgb <= 0.04045:
            return srgb / 12.92
        return ((srgb + 0.055) / 1.055) ** 2.4

    r_lum = channel_luminance(r)
    g_lum = channel_luminance(g)
    b_lum = channel_luminance(b)

    return 0.2126 * r_lum + 0.7152 * g_lum + 0.0722 * b_lum


def contrast_ratio(fg_color: str, bg_color: str) -> float:
    """Calculate WCAG contrast ratio between two colors.

    See: https://www.w3.org/TR/WCAG21/#dfn-contrast-ratio

    Args:
        fg_color: Foreground color in #RRGGBB format.
        bg_color: Background color in #RRGGBB format.

    Returns:
        Contrast ratio between 1:1 and 21:1.
    """
    lum1 = relative_luminance(fg_color)
    lum2 = relative_luminance(bg_color)

    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)

    return (lighter + 0.05) / (darker + 0.05)


# WCAG compliance thresholds
WCAG_AA_NORMAL = 4.5  # AA for normal text
WCAG_AA_LARGE = 3.0   # AA for large text (18pt+ or 14pt+ bold)
WCAG_AAA_NORMAL = 7.0  # AAA for normal text (Modus standard)
WCAG_AAA_LARGE = 4.5   # AAA for large text


def meets_wcag_aaa(fg_color: str, bg_color: str) -> bool:
    """Check if colors meet WCAG AAA for normal text (7:1).

    This is the standard Modus themes are designed to meet.

    Args:
        fg_color: Foreground color in #RRGGBB format.
        bg_color: Background color in #RRGGBB format.

    Returns:
        True if contrast ratio is at least 7:1.
    """
    return contrast_ratio(fg_color, bg_color) >= WCAG_AAA_NORMAL


def validate_palette_contrast(
    palette: dict[str, str],
    bg_key: str = "bg-main",
    fg_keys: list[str] | None = None,
) -> list[str]:
    """Validate that foreground colors have sufficient contrast with background.

    Args:
        palette: Resolved palette dictionary.
        bg_key: Key for the background color.
        fg_keys: List of foreground keys to check (defaults to common ones).

    Returns:
        List of warning messages for colors that don't meet WCAG AAA.
    """
    if fg_keys is None:
        fg_keys = [
            "fg-main", "fg-dim", "fg-alt",
            "red", "green", "blue", "yellow", "magenta", "cyan",
            "red-warmer", "green-warmer", "blue-warmer",
            "red-cooler", "green-cooler", "blue-cooler",
            "red-faint", "green-faint", "blue-faint",
            "yellow-warmer", "yellow-cooler", "yellow-faint",
            "magenta-warmer", "magenta-cooler", "magenta-faint",
            "cyan-warmer", "cyan-cooler", "cyan-faint",
        ]

    warnings: list[str] = []
    bg_color = palette.get(bg_key)

    if not bg_color or not bg_color.startswith("#"):
        return [f"Background key '{bg_key}' not found or invalid"]

    for key in fg_keys:
        fg_color = palette.get(key)
        if not fg_color or not fg_color.startswith("#"):
            continue

        ratio = contrast_ratio(fg_color, bg_color)
        if ratio < WCAG_AAA_NORMAL:
            warnings.append(
                f"{key} ({fg_color}) on {bg_key} ({bg_color}): "
                f"ratio {ratio:.2f}:1 < 7:1 (WCAG AAA)"
            )

    return warnings
