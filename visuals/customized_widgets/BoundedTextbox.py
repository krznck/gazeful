from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit

from processing.Definitions import Ref


class BoundedFloatTextbox(QLineEdit):
    def __init__(self, min: float, max: float, binding: Ref):
        super().__init__()
        self.min = min
        self.max = max
        self.fallback = binding.value
        self.binding = binding
        self.setText(str(binding.value))
        self.setAlignment(Qt.AlignmentFlag.AlignRight)

    def validate_and_correct(self):
        try:
            val = float(self.text())
            if not (self.min <= val <= self.max):
                raise ValueError
            self.binding.update(val)
        except ValueError:
            self.setText(str(self.fallback))
            self.binding.update(self.fallback)

    def focusOutEvent(self, a0: QtGui.QFocusEvent | None = None) -> None:
        self.validate_and_correct()
        super().focusOutEvent(a0)

    def keyPressEvent(self, a0: QtGui.QKeyEvent | None = None) -> None:
        if a0 is not None and a0.key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.validate_and_correct()
        super().keyPressEvent(a0)
