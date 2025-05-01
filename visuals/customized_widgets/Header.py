from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel

SIZE = 24


class Header(QLabel):
    def __init__(self, text: str) -> None:
        super().__init__(text)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.setFont(font)
