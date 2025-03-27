from PyQt6.QtGui import QPainter, QPen, QColor, QGuiApplication
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from PyQt6.QtWidgets import QWidget, QGraphicsOpacityEffect
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
_DEFAULT_FADE_ANIMATION_DURATION = 150
_DEFAULT_MOVEMENT_ANIMATION_DURATION = 50


class GazeVisualizer(QWidget):
    movement_animation: QPropertyAnimation
    previous_cords: tuple[float, float] | None
    entrance_animation: QPropertyAnimation
    exit_animation: QPropertyAnimation | None = None
    previous_cords: tuple[float, float] | None = None

    def __init__(self):
        super().__init__()
        self.setWindowTitle(_TITLE)
        self.setGeometry(0, 0, _WIDTH, _HEIGHT)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setWindowFlags(_WINDOW_FLAGS)
        self.hide()

        self.movement_animation = QPropertyAnimation(self, b"geometry")
        self.movement_animation.setDuration(_DEFAULT_MOVEMENT_ANIMATION_DURATION)

        effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(effect)

        self.entrance_animation = QPropertyAnimation(effect, b"opacity")
        self.entrance_animation.setDuration(_DEFAULT_FADE_ANIMATION_DURATION)
        self.entrance_animation.setStartValue(0)
        self.entrance_animation.setEndValue(1)
        self.entrance_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.exit_animation = QPropertyAnimation(effect, b"opacity")
        self.exit_animation.setDuration(_DEFAULT_FADE_ANIMATION_DURATION)
        self.exit_animation.setStartValue(1)
        self.exit_animation.setEndValue(0)
        self.exit_animation.finished.connect(super().hide)  # hide for realsies after finishing

    def showEvent(self, a0) -> None:
        self.entrance_animation.start()
        super().showEvent(a0)

    def hide(self) -> None:
        if not self.exit_animation:
            super().hide()
            return
        self.exit_animation.start()

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
        was_hiding = self.isHidden()

        if (x is None and y is None):
            self.hide()
            return

        assert x is not None and y is not None

        screen_width, screen_height = get_screen_size()
        scaling = get_scaling()
        x_pos = int(x * screen_width / scaling - _WIDTH / 2)
        y_pos = int(y * screen_height / scaling - _HEIGHT / 2)

        if self.previous_cords:
            pass  # TODO: Change animation depending on saccade; will need to use the real tracker for this
            # print(get_cord_difference(self.previous_cords, (x, y)))
            # Also, not really sure how to implement a saccade on a dummy mouse,
            # since a real mouse is always fixated on a specific point
        self.previous_cords = x, y

        if not was_hiding:
            self.movement_animation.stop()
            self.movement_animation.setStartValue(self.geometry())
            self.movement_animation.setEndValue(QRect(x_pos, y_pos, _HEIGHT, _WIDTH))
            self.movement_animation.start()
        else:
            self.setGeometry(x_pos, y_pos, _HEIGHT, _WIDTH)
        self.show()


def get_screen_size() -> tuple[int, int]:
    screen = QGuiApplication.primaryScreen()
    if screen is None:
        raise RuntimeError("No primary screen detected.")

    screen_geo = screen.geometry()
    return screen_geo.width(), screen_geo.height()


def get_scaling() -> float:
    screen = QGuiApplication.primaryScreen()
    if screen is None:
        raise RuntimeError("No primary screen detected.")

    return screen.devicePixelRatio()


def get_cord_difference(cords1: tuple[float, float], cords2: tuple[float, float]):
    return sqrt((cords1[0] - cords2[0])**2 + (cords1[1] - cords2[1])**2)
