"""Global application resources and default window dimensions."""
import sys
from pathlib import Path

APP_NAME: str = "Gazeful"
DEF_WIDTH: int = 1600
DEF_HEIGHT: int = 900


def get_resource_path(relative_path: str | Path) -> Path:
    """Get the absolute path to a resource, supporting both dev and PyInstaller.

    Args:
        relative_path: The path relative to the project root.

    Returns:
        The absolute path to the resource.
    """
    if hasattr(sys, "_MEIPASS"):
        # NOTE: PyInstaller creates a temp folder and stores path in _MEIPASS.
        return Path(sys._MEIPASS) / relative_path # type: ignore

    # NOTE: But in development, we use the project root (3 levels up from this file).
    return Path(__file__).parent.parent / relative_path
