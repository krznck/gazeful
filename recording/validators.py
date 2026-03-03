"""Validation utilities for file names, directories, and timestamps."""
import os
import sys
from datetime import datetime
from pathlib import Path

from appdirs import user_data_dir
from assets.resources import APP_NAME

RESERVED_NAMES_WIN = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}
RESERVED_NAMES = {".", ".."}

INVALID_CHARS_POSIX = {"/", "\0"}
INVALID_CHARS_WIN = {"<", ">", ":", '"', "/", "\\", "|", "?", "*"}

APP_DIR = Path(user_data_dir(appname=APP_NAME, appauthor=False))


def is_valid_dir(dir: str) -> bool:
    """Checks if a directory path is valid and writable.

    Args:
        dir: Path to the directory.

    Returns:
        True if the path is an absolute directory and writable.
    """
    path = Path(dir)
    if not path.is_absolute() or not path.is_dir():
        return False
    return path.exists() and os.access(path, os.W_OK)


def is_valid_filename(name: str) -> bool:
    """Checks if a string is a valid filename for the current operating system.

    Args:
        name: The filename to validate.

    Returns:
        True if the filename is valid.
    """
    if name.strip() == "":
        return False

    if any(char in name for char in INVALID_CHARS_POSIX):
        return False

    if sys.platform == "win32":
        if any(char in name for char in INVALID_CHARS_WIN):
            return False

        base = os.path.splitext(name)[0].upper()
        if base in RESERVED_NAMES_WIN:
            return False

    if name.strip() in RESERVED_NAMES:
        return False

    return True


def get_default_recording_dir() -> Path:
    """Returns the default directory for saving gaze recordings.

    Returns:
        A Path object pointing to the recordings directory in user data.
    """
    dir = APP_DIR / "recordings"
    dir.mkdir(parents=True, exist_ok=True)
    return dir


def get_default_visualization_dir() -> Path:
    """Returns the default directory for saving visualizations.

    Returns:
        A Path object pointing to the visualizations directory in user data.
    """
    dir = APP_DIR / "visualizations"
    dir.mkdir(parents=True, exist_ok=True)
    return dir


def iso_8601_time() -> str:
    """Returns the current time formatted as T%H%M (e.g., T1430).

    Returns:
        The formatted time string.
    """
    return datetime.now().strftime("T%H%M")


def iso_8601_date() -> str:
    """Returns the current date formatted as %Y-%m-%d (e.g., 2024-05-20).

    Returns:
        The formatted date string.
    """
    return datetime.now().strftime("%Y-%m-%d")
