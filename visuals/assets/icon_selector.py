"""Utilities for selecting and creating application icons."""
from enum import Enum
from pathlib import Path

from PyQt6.QtGui import QIcon

from assets.resources import get_resource_path

ICONS_DIR = Path("assets/icons")


class IconsEnum(Enum):
    """Enumeration of available SVG icons for navigation and UI."""

    HOME = "ic_fluent_home_24_regular.svg"
    CIRCLE = "ic_fluent_circle_24_regular.svg"
    RECORD = "ic_fluent_record_24_regular.svg"
    MICROSCOPE = "ic_fluent_microscope_24_regular.svg"
    BOOK_INFO = "ic_fluent_book_information_24_regular.svg"


def create_icon(choice: IconsEnum) -> QIcon:
    """Creates a QIcon object from an IconsEnum selection.

    Args:
        choice: The enum member for the desired icon.

    Returns:
        The initialized QIcon object.
    """
    path = get_resource_path(ICONS_DIR / choice.value)
    return QIcon(str(path))
