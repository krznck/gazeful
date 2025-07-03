from pathlib import Path

from PyQt6.QtGui import QScreen


def shoot_screen(screen: QScreen, path: str):
    shot = screen.grabWindow(0)  # type: ignore # NOTE: 0 means the top window, the whole

    shot.save(path, "png")
