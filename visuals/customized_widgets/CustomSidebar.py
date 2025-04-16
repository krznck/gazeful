from PyQt6.QtGui import QFontMetrics
from PyQt6.QtWidgets import QListWidget
from PyQt6.QtWidgets import QListWidgetItem
from PyQt6.QtWidgets import QWidget

PADDING = 54
FONT_SIZE = 12
SPACING = 6


class CustomSidebar(QListWidget):
    longest_text: int = 0

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.__add_styling()

    # NOTE: I couldn't get PyRight to figure out that my override is fine,
    # likely because PyQt6 does overloads via bindings and stuff. Hence, just ignore.
    def addItem(self, item: QListWidgetItem | str | None) -> None:  # type: ignore
        super().addItem(item)

        if isinstance(item, QListWidgetItem):
            self.__adjust_width(item)

    def __add_styling(self) -> None:
        font = self.font()
        font.setPointSize(FONT_SIZE)
        self.setFont(font)
        self.setSpacing(SPACING)

    def __adjust_width(self, item: QListWidgetItem) -> None:
        metrics = QFontMetrics(self.font())
        padded_length = metrics.horizontalAdvance(item.text()) + PADDING

        if padded_length > self.longest_text:
            self.setMinimumWidth(padded_length)
            self.setMaximumWidth(padded_length)
            self.longest_text = padded_length
