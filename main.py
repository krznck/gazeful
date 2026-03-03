"""Main entry point for the application."""
import argparse
import sys

from PyQt6.QtWidgets import QApplication

from AppContext import AppContext
from assets.resources import APP_NAME
from visuals.MainWindow import MainWindow


def main():
    """Parses command line arguments and launches the application."""
    parser = argparse.ArgumentParser(description=f"Run {APP_NAME}.", add_help=False)
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-d", "--developer", action="store_true", help="run in developer mode"
    )
    group.add_argument(
        "-h", "--help", action="help", help="show this help message and exit"
    )
    args = parser.parse_args()

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
