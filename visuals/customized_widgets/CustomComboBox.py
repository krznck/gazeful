"""Custom QComboBox with a standardized minimum height."""
from PyQt6.QtWidgets import QComboBox

_MIN_HEIGHT: int = 40


class CustomComboBox(QComboBox):
    """QComboBox subclass with a consistent minimum height for application UI."""

    def __init__(self) -> None:
        """Initializes the custom combo box and sets its height."""
        super().__init__()

        self.setMinimumHeight(_MIN_HEIGHT)
