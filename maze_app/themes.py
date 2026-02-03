from typing import Dict


def classic_theme() -> Dict[str, str]:
    """Return a classic color theme.

    Returns:
        A dictionary with ANSI color codes.
    """
    return {
        "entry": "\033[92m",
        "exit": "\033[91m",
        "path": "\033[93m",
        "wall": "\033[97m",
        "reset": "\033[0m"
    }


def dark_theme() -> Dict[str, str]:
    """Return a dark color theme.

    Returns:
        A dictionary with ANSI color codes.
    """
    return {
        "entry": "\033[94m",
        "exit": "\033[95m",
        "path": "\033[96m",
        "wall": "\033[38;2;30;30;30m",
        "reset": "\033[0m"
    }


def neon_theme() -> Dict[str, str]:
    """Return a neon-style color theme.

    Returns:
        A dictionary with ANSI color codes.
    """
    return {
        "entry": "\033[38;2;0;255;180m",
        "exit": "\033[38;2;255;0;200m",
        "path": "\033[38;2;180;255;0m",
        "wall": "\033[38;2;30;0;65m",
        "reset": "\033[0m"
    }
