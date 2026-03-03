"""A standardized header label for page sections."""
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel

SIZE = 24


class Header(QLabel):
    """Standardized header label with a larger, bold font."""

    def __init__(self, text: str) -> None:
        """Initializes the header label.

        Args:
            text: Header text.
        """
        super().__init__(text)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.setFont(font)
