from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget

from AppContext import AppContext
from visuals.assets.icon_selector import create_icon
from visuals.assets.icon_selector import IconsEnum


LAYOUT_ALLIGNMENT: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignTop


class InvalidInteractionError(Exception):
    """Raised when an user interface component is interacted with when that should
    not be possible.
    For example, clicking to open a directory, where no path has been chosen."""

    pass


class Page(QWidget):
    context: AppContext
    page_vbox: QVBoxLayout
    icon: QIcon | None = None

    def __init__(
        self, title: str, context: AppContext, icon: IconsEnum | None = None
    ) -> None:
        super().__init__()
        if icon is not None:
            self.icon = create_icon(icon)
        self.setWindowTitle(title)
        self.context = context
        self.page_vbox = QVBoxLayout()

        self.add_content()

        self.page_vbox.setAlignment(LAYOUT_ALLIGNMENT)
        self.setLayout(self.page_vbox)

    def add_content(self) -> None:
        pass
