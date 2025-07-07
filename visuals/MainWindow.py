from PyQt6 import QtGui
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QListWidget
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QStackedWidget
from PyQt6.QtWidgets import QWidget

from AppContext import AppContext
from assets.resources import APP_NAME
from visuals.pages.navigation import generate_navigation


class MainWindow(QMainWindow):
    sidebar: QListWidget
    pages: QStackedWidget
    context: AppContext

    def __init__(self, context: AppContext) -> None:
        super().__init__()
        self.context = context
        self.setWindowTitle(APP_NAME)

        self.sidebar = QListWidget()
        self.pages = QStackedWidget()
        self.sidebar, self.pages = generate_navigation(context)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.pages)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def closeEvent(self, a0: QtGui.QCloseEvent | None = None) -> None:
        self.context.disconnect_tracker()
        return super().closeEvent(a0)
