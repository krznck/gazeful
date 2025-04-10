from PyQt6.QtCore import QPropertyAnimation
from PyQt6.QtCore import QRect
from PyQt6.QtGui import QPainter
from PyQt6.QtGui import QPen
from PyQt6.QtGui import QScreen
from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import QGraphicsOpacityEffect
from PyQt6.QtWidgets import QWidget

from trackers.GazePoint import GazePoint
from visuals.visualizer import constants
from visuals.visualizer.VelocityCalculator import VelocityCalculator


class GazeVisualizer(QWidget):
    movement_animation: QPropertyAnimation
    entrance_animation: QPropertyAnimation
    exit_animation: QPropertyAnimation
    bound_screen: QScreen
    velocity_calc: VelocityCalculator
    last_x, last_y = 0, 0

    def __init__(self, screen: QScreen):
        super().__init__()

        self.velocity_calc = VelocityCalculator()

        self.bound_screen = screen

        self.setWindowTitle(constants.TITLE)
        self.setGeometry(0, 0, constants.WIDTH, constants.HEIGHT)
        for attribute in constants.WIDGET_ATTRIBUTES:
            self.setAttribute(attribute)
        self.setWindowFlags(constants.WINDOW_FLAGS)
        self.hide()

        self.movement_animation = QPropertyAnimation(self, b"geometry")
        self.movement_animation.setEasingCurve(
            constants.MOVEMENT_ANIMATION_EASING_CURVE
        )

        effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(effect)

        self.entrance_animation = QPropertyAnimation(effect, b"opacity")
        self.entrance_animation.setDuration(constants.DEFAULT_FADE_ANIMATION_DURATION)
        self.entrance_animation.setStartValue(0)
        self.entrance_animation.setEndValue(1)
        self.entrance_animation.setEasingCurve(
            constants.ENTRANCE_ANIMATION_EASING_CURVE
        )

        self.exit_animation = QPropertyAnimation(effect, b"opacity")
        self.exit_animation.setDuration(constants.DEFAULT_FADE_ANIMATION_DURATION)
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
        painter.setRenderHint(constants.RING_RENDER_HINT)

        pen = QPen()
        pen.setStyle(constants.RING_STYLE)
        pen.setColor(constants.RING_COLOR)
        pen.setWidth(constants.RING_THICKNESS)

        painter.setPen(pen)

        margin = constants.RING_MARGIN
        width = int(constants.WIDTH * (1 - margin))
        height = int(constants.HEIGHT * (1 - margin))
        x = int((constants.WIDTH - width) / 2)
        y = int((constants.HEIGHT - height) / 2)

        painter.drawEllipse(x, y, width, height)

    def set_position(self, gaze: GazePoint):
        self.velocity_calc.update(gaze)

        was_hiding = self.isHidden()

        x, y = gaze.x, gaze.y

        if gaze.are_eyes_closed():
            self.hide()
            return

        assert x is not None and y is not None

        screen = self.bound_screen
        geometry = screen.geometry()

        screen_x = geometry.x()
        screen_y = geometry.y()
        screen_width = geometry.width()
        screen_height = geometry.height()

        x_pos = int(screen_x + x * screen_width - constants.WIDTH / 2)
        y_pos = int(screen_y + y * screen_height - constants.HEIGHT / 2)

        position_changed = self.last_x != x_pos or self.last_y != y_pos

        self.last_x, self.last_y = x_pos, y_pos

        if not was_hiding:
            if position_changed:
                self.movement_animation.stop()
                self.movement_animation.setDuration(
                    get_animation_duration(self.velocity_calc.velocity)
                )
                self.movement_animation.setStartValue(self.geometry())
                self.movement_animation.setEndValue(
                    QRect(x_pos, y_pos, constants.WIDTH, constants.HEIGHT)
                )
                self.movement_animation.start()
        else:
            self.setGeometry(x_pos, y_pos, constants.WIDTH, constants.HEIGHT)

        self.show()


def get_animation_duration(velocity: float) -> int:
    min_duration = constants.MIN_MOVEMENT_ANIMATION_DURATION
    max_duration = constants.MAX_MOVEMENT_ANIMATION_DURATION
    falloff = constants.MOVEMENT_ANIMATION_DURATION_FALLOFF

    duration = int(
        min_duration + (max_duration - min_duration) / (1 + (velocity * falloff))
    )
    # print("Animation duration: " + str(duration))
    return duration
