"""Custom QPushButton with a standardized minimum height."""
from PyQt6.QtWidgets import QPushButton

_MIN_HEIGHT: int = 35


class CustomPushButton(QPushButton):
    """QPushButton subclass with a consistent minimum height for application UI."""

    def __init__(self, text: str | None = None):
        """Initializes the custom push button.

        Args:
            text: Optional text to display on the button.
        """
        super().__init__(text)

        self.setMinimumHeight(_MIN_HEIGHT)
