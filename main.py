import argparse
import os
import sys

from PyQt6.QtWidgets import QApplication

from AppContext import AppContext
from assets.resources import APP_NAME
from visuals.MainWindow import MainWindow


def main():
    parser = argparse.ArgumentParser(description=f"Run {APP_NAME}.", add_help=False)
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-d", "--developer", action="store_true", help="run in developer mode"
    )
    group.add_argument(
        "-h", "--help", action="help", help="show this help message and exit"
    )
    args = parser.parse_args()

    # NOTE:
    # The Gaze Visualizer will break on Wayland, due to Wayland disallowing anything
    # other than the compositor from moving windows. By setting this environment
    # variable, we tell Qt to use the X C-bindings instead, and use the XWayland
    # compatibility layer. This does not fix screenshotting on Wayland however, sadly.
    if sys.platform == "linux":
        os.environ["QT_QPA_PLATFORM"] = "xcb"

    app = QApplication([])
    context = AppContext()
    if args.developer:
        window = MainWindow(context, inspection=True)
    else:
        window = MainWindow(context)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
