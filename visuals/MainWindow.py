"""Main window implementation for the nnetp application."""
from AppContext import AppContext
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QListWidget,
                             QMainWindow, QStackedWidget, QWidget)

from assets.resources import APP_NAME, DEF_HEIGHT, DEF_WIDTH
from visuals.pages.navigation import generate_navigation


class MainWindow(QMainWindow):
    """The primary application window coordinating navigation and page display.

    Attributes:
        sidebar: The sidebar widget for navigation.
        pages: The stacked widget containing all application pages.
        context: The global application context.
    """

    sidebar: QListWidget
    pages: QStackedWidget
    context: AppContext

    def __init__(self, context: AppContext, inspection: bool = False) -> None:
        """Initializes the main window and its layout.

        Args:
            context: The application context.
            inspection: Whether to enable the widget inspector tool.
        """
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
        """Handles the window close event by disconnecting the tracker.

        Args:
            a0: The close event.
        """
        self.context.disconnect_tracker()
        return super().closeEvent(a0)

    def keyPressEvent(self, a0: QtGui.QKeyEvent | None) -> None:
        """Handles global key shortcuts, including the inspector toggle.

        Args:
            a0: The key event.
        """
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
        """Prints diagnostic information about the widget currently under the cursor."""
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
