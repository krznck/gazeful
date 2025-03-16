from PyQt6.QtGui import QPainter, QPen, QColor, QGuiApplication
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect
from PyQt6.QtWidgets import QWidget
from math import sqrt

_TITLE = "Gaze Visualizer Window"
_WIDTH = _HEIGHT = 100
_OPACITY = 153  # out of 255
_RED = QColor(255, 0, 0, _OPACITY)
_THICKNESS = 3
_MARGIN = 0.1
_WINDOW_FLAGS = (
    Qt.WindowType.Tool
    | Qt.WindowType.WindowStaysOnTopHint
    | Qt.WindowType.FramelessWindowHint
    )
_DEFAULT_ANIMATION_DURATION = 50


class GazeVisualizer(QWidget):
    animation: QPropertyAnimation
    previous_cords: tuple[float, float] | None

    def __init__(self):
        super().__init__()
        self.setWindowTitle(_TITLE)
        self.setGeometry(0, 0, _WIDTH, _HEIGHT)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setWindowFlags(_WINDOW_FLAGS)
        self.hide()

        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(_DEFAULT_ANIMATION_DURATION)
        self.previous_cords = None

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

        if self.previous_cords:
            pass  # TODO: Change animation depending on saccade; will need to use the real tracker for this
            # print(get_cord_difference(self.previous_cords, (x, y)))
            # Also, not really sure how to implement a saccade on a dummy mouse,
            # since a real mouse is always fixated on a specific point
        self.previous_cords = x, y

        self.animation.stop()
        self.animation.setStartValue(self.geometry())
        self.animation.setEndValue(QRect(x_pos, y_pos, _HEIGHT, _WIDTH))
        self.animation.start()
        self.show()


def get_screen_size() -> tuple[int, int]:
    screen = QGuiApplication.primaryScreen()
    if screen is None:
        raise RuntimeError("No primary screen detected.")

    screen_geo = screen.geometry()
    return screen_geo.width(), screen_geo.height()


def get_cord_difference(cords1: tuple[float, float], cords2: tuple[float, float]):
    return sqrt((cords1[0] - cords2[0])**2 + (cords1[1] - cords2[1])**2)
