"""Real-time gaze visualizer overlay widget."""
from PyQt6.QtCore import QPropertyAnimation, QRect
from PyQt6.QtGui import QColor, QPainter, QPen, QScreen, QShowEvent
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QWidget
from trackers.GazePoint import GazePoint

from visuals.visualizer import constants
from visuals.visualizer.VelocityCalculator import VelocityCalculator


class GazeVisualizer(QWidget):
    """A translucent overlay widget that displays the user's gaze position in real-time.

    Supports smooth movement animations, entrance/exit fades, and dynamic opacity
    control.

    Attributes:
        movement_animation: Animation for moving the widget between coordinates.
        entrance_animation: Fade-in animation when the widget appears.
        exit_animation: Fade-out animation when the widget disappears.
        bound_screen: The screen where the visualizer is currently displayed.
        velocity_calc: Tool for calculating movement speed to adjust animation duration.
        animations: Whether animations are currently enabled.
        opacity: The alpha value (0-255) for the visualizer ring.
        enabled: Whether the visualizer is allowed to be shown.
    """

    movement_animation: QPropertyAnimation
    entrance_animation: QPropertyAnimation
    exit_animation: QPropertyAnimation
    bound_screen: QScreen
    velocity_calc: VelocityCalculator
    last_x, last_y = 0, 0
    animations: bool
    opacity: int = constants.OPACITY

    enabled: bool = False

    def __init__(self, screen: QScreen, animations: bool = True):
        """Initializes the gaze visualizer.

        Args:
            screen: The monitor to display the visualizer on.
            animations: Whether to enable movement and fade animations.
        """
        super().__init__()

        self.velocity_calc = VelocityCalculator()

        self.bound_screen = screen
        self.animations = animations

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

    def toggle(self, on: bool) -> None:
        """Enables or disables the visualizer.

        Args:
            on: New enabled state.
        """
        self.enabled = on
        if not on:
            self.hide()

    def showEvent(self, a0: QShowEvent | None) -> None:
        """Handles the show event, triggering the entrance animation if enabled.

        Args:
            a0: The show event.
        """
        if self.animations:
            self.entrance_animation.start()
        super().showEvent(a0)

    def hide(self) -> None:
        """Hides the visualizer, triggering the exit fade if enabled."""
        if (
            not hasattr(self, "exit_animation")
            or self.exit_animation is None
            or not self.animations
        ):
            super().hide()
            return
        self.exit_animation.start()

    def paintEvent(self, a0) -> None:
        """Paints the visualizer ring onto the widget.

        Args:
            a0: The paint event.
        """
        _ = a0  # required by method override, unused

        painter = QPainter(self)
        painter.setRenderHint(constants.RING_RENDER_HINT)

        pen = QPen()
        pen.setStyle(constants.RING_STYLE)
        pen.setColor(QColor(*constants.RING_COLOR, self.opacity))
        pen.setWidth(constants.RING_THICKNESS)

        painter.setPen(pen)

        margin = constants.RING_MARGIN
        width = int(constants.WIDTH * (1 - margin))
        height = int(constants.HEIGHT * (1 - margin))
        x = int((constants.WIDTH - width) / 2)
        y = int((constants.HEIGHT - height) / 2)

        painter.drawEllipse(x, y, width, height)

    def set_position(self, gaze: GazePoint):
        """Updates the visualizer position based on a normalized GazePoint.

        Translates normalized (0.0 to 1.0) coordinates to absolute screen pixels.

        Args:
            gaze: The gaze point containing current eye position.
        """
        if not self.enabled:
            return

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

        if not was_hiding and self.animations:
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

    def set_opacity(self, opacity: int) -> None:
        """Updates the visualizer's transparency.

        Args:
            opacity: Alpha value from 0 (transparent) to 255 (opaque).
        """
        self.opacity = max(0, min(255, opacity))
        self.update()

    def toggle_animations(self, on: bool | None = None) -> None:
        """Toggles the state of animations.

        Args:
            on: Optional explicit state. If None, toggles current state.
        """
        if isinstance(on, bool):
            self.animations = on
        else:
            self.animations = not self.animations


def get_animation_duration(velocity: float) -> int:
    """Calculates movement animation duration based on gaze velocity.

    Faster movements result in shorter animation durations for a 'snappier' feel.

    Args:
        velocity: Current gaze velocity.

    Returns:
        Duration in milliseconds.
    """
    min_duration = constants.MIN_MOVEMENT_ANIMATION_DURATION
    max_duration = constants.MAX_MOVEMENT_ANIMATION_DURATION
    falloff = constants.MOVEMENT_ANIMATION_DURATION_FALLOFF

    duration = int(
        min_duration + (max_duration - min_duration) / (1 + (velocity * falloff))
    )
    # print("Animation duration: " + str(duration))
    return duration
