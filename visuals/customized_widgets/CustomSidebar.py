"""A styled navigation sidebar that dynamically adjusts its width."""
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QWidget

PADDING = 54
FONT_SIZE = 12
SPACING = 6


class CustomSidebar(QListWidget):
    """QListWidget subclass representing the main application navigation bar.

    The sidebar automatically adjusts its width to accommodate the longest
    navigation item label.

    Attributes:
        longest_text: Current maximum width encountered among items.
    """

    longest_text: int = 0

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initializes the sidebar and applies custom styling.

        Args:
            parent: Parent widget.
        """
        super().__init__(parent)
        self.__add_styling()

    # NOTE: I couldn't get PyRight to figure out that my override is fine,
    # likely because PyQt6 does overloads via bindings and stuff. Hence, just ignore.
    def addItem(self, item: QListWidgetItem | str | None) -> None:  # type: ignore
        """Adds an item to the sidebar and adjusts its width.

        Args:
            item: The item or text label to add.
        """
        super().addItem(item)

        if isinstance(item, QListWidgetItem):
            self.__adjust_width(item)

    def __add_styling(self) -> None:
        """Applies font and spacing styles to the sidebar."""
        font = self.font()
        font.setPointSize(FONT_SIZE)
        self.setFont(font)
        self.setSpacing(SPACING)

    def __adjust_width(self, item: QListWidgetItem) -> None:
        """Recalculates and updates the sidebar width for a new item.

        Args:
            item: The item whose label length is used for calculation.
        """
        metrics = QFontMetrics(self.font())
        padded_length = metrics.horizontalAdvance(item.text()) + PADDING

        if padded_length > self.longest_text:
            self.setMinimumWidth(padded_length)
            self.setMaximumWidth(padded_length)
            self.longest_text = padded_length
