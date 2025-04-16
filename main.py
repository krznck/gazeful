import sys

from PyQt6.QtWidgets import QApplication

from AppContext import AppContext
from visuals.MainWindow import MainWindow


def main():
    app = QApplication([])

    context = AppContext()
    window = MainWindow(context)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
