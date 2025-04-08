from pynput import mouse

from trackers.Tracker import Tracker
from visuals.GazeVisualizer import GazeVisualizer


class MouseTracker(Tracker):
    left_held: bool = False
    right_held: bool = False

    def __init__(self, visualizer: GazeVisualizer | None = None) -> None:
        super().__init__(visualizer)
        self.listener = mouse.Listener(
            on_move=self.__on_move, on_click=self.__on_click  # type: ignore
        )

    def run(self):
        self.listener.start()
        self.listener.join()

    def __on_click(self, button: mouse.Button) -> None:
        if button is mouse.Button.left:
            self.left_held = not self.left_held
        if button is mouse.Button.right:
            self.right_held = not self.right_held

    def __are_eyes_closed(self) -> bool:
        return self.right_held and self.left_held

    def __on_move(self, x: float, y: float) -> None:
        if self.visualizer is None:
            return

        if self.__are_eyes_closed():
            self.eyes_position_changed.emit(None, None)
            return

        # NOTE: little trick here - a real eyetracker has a specific
        # region (ergo, a screen) that it's tracking within, but your cursor
        # can be anywhere.
        # Hence, where for a real tracker the bound screen is only used to inidcate
        # which screen we should be visualizing on, the dummy tracker uses it to
        # know what we are pretending to be tracking in the first place
        screen = self.visualizer.bound_screen
        geometry = screen.geometry()
        scaling = screen.devicePixelRatio()

        screen_x = geometry.x()
        screen_y = geometry.y()
        screen_width = geometry.width() * scaling
        screen_height = geometry.height() * scaling

        # when you're not looking within the constraints of the eyetracking region,
        # that would be analogous to the eyetracker thinking your eyes are closed
        if not (
            screen_x <= x <= screen_x + screen_width
            and screen_y <= y <= screen_y + screen_height
        ):
            self.eyes_position_changed.emit(None, None)
            return

        relative_x = x - screen_x
        relative_y = y - screen_y
        norm_x = relative_x / screen_width
        norm_y = relative_y / screen_height

        self.eyes_position_changed.emit(norm_x, norm_y)
