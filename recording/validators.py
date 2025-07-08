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


def is_valid_dir(dir: str) -> bool:
    path = Path(dir)
    if not path.is_absolute() or not path.is_dir():
        return False
    return path.exists() and os.access(path, os.W_OK)


def is_valid_filename(name: str) -> bool:
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


def get_default_recording_dir() -> str:
    dir = Path(user_data_dir(appname=APP_NAME, appauthor=False))
    dir = dir / "recordings" / f"gaze-session-{iso_8601_date()}"
    dir.mkdir(parents=True, exist_ok=True)
    return str(dir)


def get_default_visualization_dir() -> str:
    dir = Path(user_data_dir(appname=APP_NAME, appauthor=False))
    dir = dir / "visualizations" / f"visualization-{iso_8601_date()}"
    dir.mkdir(parents=True, exist_ok=True)
    return str(dir)


def iso_8601_time() -> str:
    return datetime.now().strftime("T%H%M")


def iso_8601_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")
