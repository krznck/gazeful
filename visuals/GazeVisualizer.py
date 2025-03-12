from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor, QGuiApplication
from PyQt6.QtCore import Qt

_TITLE = "Gaze Visualizer Window"
_WIDTH = _HEIGHT = 100
_RED = QColor(255, 0, 0)
_THICKNESS = 2
_MARGIN = 0.1


class GazeVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(_TITLE)
        self.setGeometry(0, 0, _WIDTH, _HEIGHT)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.WindowStaysOnTopHint |
                            Qt.WindowType.Tool)
        self.hide()

    def paintEvent(self, a0):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        pen = QPen()
        pen.setStyle(Qt.PenStyle.SolidLine)
        pen.setColor(_RED)
        pen.setWidth(_THICKNESS)

        painter.setPen(pen)

        margin = _MARGIN
        width = int(_WIDTH * (1 - margin))
        height = int(_HEIGHT * (1 - margin))
        x = int((_WIDTH - width) / 2)
        y = int((_HEIGHT - height) / 2)

        painter.drawEllipse(x, y, width, height)

    def set_position(self, x: float | None, y: float | None):
        if (x is None and y is None):
            self.hide()
            return

        assert x is not None and y is not None

        screen_width, screen_height = get_screen_size()
        x_pos = int(x * screen_width - _WIDTH / 2)
        y_pos = int(y * screen_height - _HEIGHT / 2)

        self.setGeometry(x_pos, y_pos, _HEIGHT, _WIDTH)
        self.show()


def get_screen_size() -> tuple[int, int]:
    screen = QGuiApplication.primaryScreen()
    if screen is None:
        raise RuntimeError("No primary screen detected.")

    screen_geo = screen.geometry()
    return screen_geo.width(), screen_geo.height()
