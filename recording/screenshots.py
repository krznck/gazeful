from pathlib import Path
from PyQt6.QtGui import QScreen
import os


def shoot_screen(screen: QScreen, path: Path):
    shot = screen.grabWindow(0)  # type: ignore # NOTE: 0 means top window, the whole

    path.parent.mkdir(parents=True, exist_ok=True)
    if not shot.save(str(path), "png"):
        if os.environ.get("WAYLAND_DISPLAY"):
            raise RuntimeError("Screen capture is not permitted on Wayland")
        raise RuntimeError(f"Failed to save screenshot at {path}")
