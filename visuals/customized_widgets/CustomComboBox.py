from PyQt6.QtWidgets import QComboBox

_MIN_HEIGHT: int = 40


class CustomComboBox(QComboBox):
    def __init__(self) -> None:
        super().__init__()

        self.setMinimumHeight(_MIN_HEIGHT)
