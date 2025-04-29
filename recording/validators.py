import os
import sys
from pathlib import Path

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
