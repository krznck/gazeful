import random
import time

from pynput import mouse
from PyQt6.QtCore import QMetaObject
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QCursor

import screens
from trackers.GazePoint import GazePoint
from trackers.Tracker import Tracker
from visuals.visualizer.GazeVisualizer import GazeVisualizer

DEFAULT_FREQUENCY = 60
MIN_TREMOR_TRESHHOLD: int = 1
MAX_TREMOR_TRESHHOLD: int = 7


class MouseTracker(Tracker):
    left_held: bool = False
    right_held: bool = False
    last_update_time: float = 0.0
    simulated_frequency: int = DEFAULT_FREQUENCY  # hertz
    timer: QTimer | None = None
    listener: mouse.Listener

    def __init__(self, visualizer: GazeVisualizer) -> None:
        super().__init__(visualizer)
        self.listener = mouse.Listener(on_click=self.__on_click)  # type: ignore

    def run(self):
        self.listener.start()

        self.timer = QTimer()
        self.timer.timeout.connect(self.__poll_mouse)
        self.timer.setInterval(int(1000 / self.simulated_frequency))  # milliseconds
        self.timer.start()

        self.exec()

    def stop(self) -> None:
        self.__cleanup_timer()
        self.listener.stop()
        super().stop()

    def __on_click(self, x, y, button: mouse.Button) -> None:
        # NOTE: method needs x and y in order to pass button correctly,
        # but we're not using it anyway
        _ = x, y
        if button is mouse.Button.left:
            self.left_held = not self.left_held
        if button is mouse.Button.right:
            self.right_held = not self.right_held

    def __are_eyes_closed(self) -> bool:
        return self.right_held and self.left_held

    def __poll_mouse(self):
        if self.visualizer is None:
            return

        gaze = GazePoint(timestamp=time.monotonic())

        if self.__are_eyes_closed():
            self.eyes_position_changed.emit(gaze)
            return

        position = QCursor.pos()
        x, y = position.x(), position.y()
        x, y = add_tremor(x), add_tremor(y)

        # NOTE: This is a little trick.
        # A real eyetracker is already bound to a physical screen,
        # but your cursor can be anywhere, so the dummy needs to be told which screen
        # to simulate tracking on. Hence we secretely use the visualizer's bound screen.
        scr_x, scr_y, scr_width, scr_height = screens.get_geometry(
            self.visualizer.bound_screen
        )  # scr == screen, if it wasn't obvious

        # when you're not looking within the constraints of the eyetracking region,
        # that would be analogous to the eyetracker thinking your eyes are closed
        if not (scr_x <= x <= scr_x + scr_width and scr_y <= y <= scr_y + scr_height):
            self.eyes_position_changed.emit(gaze)
            return

        relative_x = x - scr_x
        relative_y = y - scr_y
        gaze.x = relative_x / scr_width
        gaze.y = relative_y / scr_height

        # print("Gaze: " + str(gaze))
        self.eyes_position_changed.emit(gaze)

    def __cleanup_timer(self):
        if self.timer is not None:
            QMetaObject.invokeMethod(
                self.timer, "stop", Qt.ConnectionType.QueuedConnection
            )
            QMetaObject.invokeMethod(
                self.timer, "deleteLater", Qt.ConnectionType.QueuedConnection
            )
            self.timer = None


def add_tremor(position: int) -> float:
    treshhold = random.randint(MIN_TREMOR_TRESHHOLD, MAX_TREMOR_TRESHHOLD)
    new = position
    offset = random.gauss(0, treshhold)

    # print("Tremor value: " + str(offset))
    return new + offset
