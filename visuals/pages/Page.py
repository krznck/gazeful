from abc import abstractmethod
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget

from visuals.assets.icon_selector import create_icon
from visuals.assets.icon_selector import IconsEnum


LAYOUT_ALLIGNMENT: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignTop


class InvalidInteractionError(Exception):
    """Raised when an user interface component is interacted with when that should
    not be possible.
    For example, clicking to open a directory, where no path has been chosen."""

    pass


class Page(QWidget):
    icon: QIcon | None = None
    _page_vbox: QVBoxLayout

    def __init__(self, title: str, icon: IconsEnum | None = None) -> None:
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
        pass
