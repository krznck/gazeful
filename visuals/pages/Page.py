"""Base class and common definitions for all application pages."""
from abc import abstractmethod

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from visuals.assets.icon_selector import IconsEnum, create_icon

LAYOUT_ALLIGNMENT: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignTop


class InvalidInteractionError(Exception):
    """Raised when a user interface component is interacted with unexpectedly.

    For example, clicking to open a directory when no path has been chosen.
    """

    pass


class Page(QWidget):
    """Abstract base class for all UI pages in the application.

    Attributes:
        icon: Optional icon representing the page.
        _page_vbox: Main vertical layout for page content.
    """

    icon: QIcon | None = None
    _page_vbox: QVBoxLayout

    def __init__(self, title: str, icon: IconsEnum | None = None) -> None:
        """Initializes the page and its layout.

        Args:
            title: Title of the page.
            icon: Icon to display in the navigation sidebar.
        """
        super().__init__()
        if icon is not None:
            self.icon = create_icon(icon)
        self.setWindowTitle(title)
        self._page_vbox = QVBoxLayout()

        self.add_content()

        self._page_vbox.setAlignment(LAYOUT_ALLIGNMENT)
        self.setLayout(self._page_vbox)

    @abstractmethod
    def add_content(self) -> None:
        """Abstract method to define and add UI components to the page."""
        pass
