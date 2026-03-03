"""Functions for capturing and saving screen images."""
import os
from pathlib import Path

from PyQt6.QtGui import QScreen


def shoot_screen(screen: QScreen, path: Path):
    """Captures a screenshot of the specified screen and saves it to a file.

    Args:
        screen: The screen to capture.
        path: Destination path for the screenshot image.

    Raises:
        RuntimeError: If capturing the screenshot fails, or if it's attempted on Wayland.
    """
    shot = screen.grabWindow(0)  # type: ignore # NOTE: 0 means top window, the whole

    path.parent.mkdir(parents=True, exist_ok=True)
    if not shot.save(str(path), "png"):
        if os.environ.get("WAYLAND_DISPLAY"):
            raise RuntimeError("Screen capture is not permitted on Wayland")
        raise RuntimeError(f"Failed to save screenshot at {path}")
