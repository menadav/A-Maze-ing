def classic_theme():
    """Return the classic color theme."""
    return {
        "entry": "\033[92m",
        "exit": "\033[91m",
        "path": "\033[93m",
        "wall": "\033[97m",
        "reset": "\033[0m"
    }

def dark_theme():
    """Return the dark color theme."""
    return {
        "entry": "\033[94m",
        "exit": "\033[95m",
        "path": "\033[96m",
        "wall": "\033[90m",
        "reset": "\033[0m"
    }

def forest_theme():
    """Return the forest color theme."""
    return {
        "entry": "\033[38;2;0;180;0m",
        "exit": "\033[38;2;180;30;30m",
        "path": "\033[38;2;200;150;0m",
        "wall": "\033[38;2;120;80;40m",
        "reset": "\033[0m"
    }

def neon_theme():
    """Return the neon color theme."""
    return {
        "entry": "\033[38;2;255;0;255m",
        "exit": "\033[38;2;255;120;0m",
        "path": "\033[38;2;0;255;255m",
        "wall": "\033[38;2;255;255;255m",
        "reset": "\033[0m"
    }
