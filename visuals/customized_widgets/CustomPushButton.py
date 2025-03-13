from PyQt6.QtWidgets import QPushButton

_MIN_HEIGHT: int = 35


class CustomPushButton(QPushButton):
    def __init__(self, text: str | None = None):
        super().__init__(text)

        self.setMinimumHeight(_MIN_HEIGHT)
