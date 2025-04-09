from math import sqrt

from PyQt6.QtCore import QEasingCurve
from PyQt6.QtCore import QPropertyAnimation
from PyQt6.QtCore import QRect
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtGui import QPainter
from PyQt6.QtGui import QPen
from PyQt6.QtGui import QScreen
from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import QGraphicsOpacityEffect
from PyQt6.QtWidgets import QWidget

from trackers.GazePoint import GazePoint
from visuals.VelocityCalculator import VelocityCalculator

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
_DEFAULT_MOVEMENT_ANIMATION_DURATION = 100


class GazeVisualizer(QWidget):
    movement_animation: QPropertyAnimation
    entrance_animation: QPropertyAnimation
    exit_animation: QPropertyAnimation
    previous_cords: tuple[float, float] | None = None
    bound_screen: QScreen
    velocity_calc: VelocityCalculator

    def __init__(self, screen: QScreen):
        super().__init__()

        self.velocity_calc = VelocityCalculator()

        self.bound_screen = screen

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

        self.exit_animation.finished.connect(
            super().hide
        )  # hide for realsies after finishing

    def showEvent(self, a0: QShowEvent | None) -> None:
        self.entrance_animation.start()
        super().showEvent(a0)

    def hide(self) -> None:
        if not hasattr(self, "exit_animation") or self.exit_animation is None:
            super().hide()
            return
        self.exit_animation.start()

    def paintEvent(self, a0) -> None:
        _ = a0  # required by method override, unused

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

    # TODO: add detecting saccades and having the animation behave differently with that
    def set_position(self, gaze: GazePoint):
        self.velocity_calc.update(gaze)

        was_hiding = self.isHidden()

        x, y = gaze.x, gaze.y

        if x is None and y is None:
            self.hide()
            return

        assert x is not None and y is not None

        screen = self.bound_screen
        geometry = screen.geometry()

        screen_x = geometry.x()
        screen_y = geometry.y()
        screen_width = geometry.width()
        screen_height = geometry.height()

        x_pos = int(screen_x + x * screen_width - _WIDTH / 2)
        y_pos = int(screen_y + y * screen_height - _HEIGHT / 2)

        self.previous_cords = x, y

        if not was_hiding:
            self.movement_animation.stop()
            self.movement_animation.setStartValue(self.geometry())
            self.movement_animation.setEndValue(QRect(x_pos, y_pos, _HEIGHT, _WIDTH))
            self.movement_animation.start()
        else:
            self.setGeometry(x_pos, y_pos, _HEIGHT, _WIDTH)
        self.show()


def get_cord_difference(cords1: tuple[float, float], cords2: tuple[float, float]):
    return sqrt((cords1[0] - cords2[0]) ** 2 + (cords1[1] - cords2[1]) ** 2)
