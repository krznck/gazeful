from PyQt6 import QtCore
from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QListWidget
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QStackedWidget
from PyQt6.QtWidgets import QWidget

from AppContext import AppContext
from assets.resources import APP_NAME, DEF_HEIGHT, DEF_WIDTH
from visuals.pages.navigation import generate_navigation


class MainWindow(QMainWindow):
    sidebar: QListWidget
    pages: QStackedWidget
    context: AppContext

    def __init__(self, context: AppContext, inspection: bool = False) -> None:
        super().__init__()
        self.context = context
        self.setWindowTitle(APP_NAME)
        self.resize(DEF_WIDTH, DEF_HEIGHT)

        self.sidebar = QListWidget()
        self.pages = QStackedWidget()
        self.sidebar, self.pages = generate_navigation(context)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.pages)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self._inspection = inspection

    def closeEvent(self, a0: QtGui.QCloseEvent | None = None) -> None:
        self.context.disconnect_tracker()
        return super().closeEvent(a0)

    def keyPressEvent(self, a0: QtGui.QKeyEvent | None) -> None:
        if a0 is None:
            return

        # pressing Control Shift I
        if (
            self._inspection
            and a0.key() == Qt.Key.Key_I
            and a0.modifiers()
            == (
                QtCore.Qt.KeyboardModifier.ControlModifier
                | QtCore.Qt.KeyboardModifier.ShiftModifier
            )
        ):
            return self.inspect_widget_at_cursor()

        return super().keyPressEvent(a0)

    def inspect_widget_at_cursor(self):
        pos = QtGui.QCursor.pos()
        widget = QApplication.widgetAt(pos)

        if not widget:
            print("No wdiget found under the cursor")
            return

        print("-- Widget Inspector ---")
        print(f"Inspecting widget at screen position {pos.x()}, {pos.y()}\n")

        current = widget
        indent = 0
        while current:
            class_name = current.__class__.__name__
            obj_name = current.objectName()

            prefix = " " * indent
            print(f"{prefix} -> Class: {class_name}, Name: '{obj_name or 'Not Set'}'")

            current = current.parent()
            indent += 1
        print("-" * 24)
