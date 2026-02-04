#!/usr/bin/env python3
"""Path utilities for Modus theme ports."""

from __future__ import annotations

import os
from pathlib import Path


def xdg_config_home() -> Path:
    """Return the XDG config home directory.

    Returns $XDG_CONFIG_HOME if set, otherwise ~/.config.
    """
    return Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
