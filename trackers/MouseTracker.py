import time

from pynput import mouse

import screens
from trackers.GazePoint import GazePoint
from trackers.Tracker import Tracker
from visuals.GazeVisualizer import GazeVisualizer


class MouseTracker(Tracker):
    left_held: bool = False
    right_held: bool = False
    last_update_time: float = 0.0
    simulated_frequency: int = 60  # hertz

    def __init__(self, visualizer: GazeVisualizer | None = None) -> None:
        super().__init__(visualizer)
        self.listener = mouse.Listener(
            on_move=self.__on_move, on_click=self.__on_click  # type: ignore
        )

    def run(self):
        self.listener.start()
        self.listener.join()

    def __on_click(self, x: float, y: float, button: mouse.Button) -> None:
        # NOTE: method needs x and y in order to pass button correctly,
        # but we're not using it anyway
        _ = x, y
        if button is mouse.Button.left:
            self.left_held = not self.left_held
        if button is mouse.Button.right:
            self.right_held = not self.right_held

    def __are_eyes_closed(self) -> bool:
        return self.right_held and self.left_held

    def __on_move(self, x: float, y: float) -> None:
        if self.visualizer is None:
            return

        gaze = GazePoint(timestamp=time.time())

        if not self.__can_update(gaze.timestamp):
            return

        if self.__are_eyes_closed():
            self.eyes_position_changed.emit(gaze)
            return

        # NOTE: little trick here - a real eyetracker has a specific
        # region (ergo, a screen) that it's tracking within, but your cursor
        # can be anywhere.
        # Hence, where for a real tracker the bound screen is only used to inidcate
        # which screen we should be visualizing on, the dummy tracker uses it to
        # know what we are pretending to be tracking in the first place

        # scr == screen, if it wasn't obvious
        scr_x, scr_y, scr_width, scr_height = screens.get_scaled_geometry(
            self.visualizer.bound_screen
        )

        # when you're not looking within the constraints of the eyetracking region,
        # that would be analogous to the eyetracker thinking your eyes are closed
        if not (scr_x <= x <= scr_x + scr_width and scr_y <= y <= scr_y + scr_height):
            self.eyes_position_changed.emit(gaze)
            return

        relative_x = x - scr_x
        relative_y = y - scr_y
        gaze.x = relative_x / scr_width
        gaze.y = relative_y / scr_height

        self.eyes_position_changed.emit(gaze)

    def __can_update(self, time: float) -> bool:
        """Simulates frequency of a real eyetracker by declaring that an update is not
        allowed unless enough time has passed."""
        if time - self.last_update_time < (1.0 / self.simulated_frequency):
            return False

        self.last_update_time = time
        return True
