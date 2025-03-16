from visuals.GazeVisualizer import get_screen_size
from visuals.GazeVisualizer import GazeVisualizer
from trackers.Tracker import Tracker
from pynput import mouse


class MouseTracker(Tracker):
    left_held: bool = False
    right_held: bool = False

    def __init__(self, visualizer: GazeVisualizer | None = None) -> None:
        super().__init__(visualizer)
        self.listener = mouse.Listener(
            on_move=self.__on_move, on_click=self.__on_click)  # type: ignore

    def run(self):
        self.listener.start()
        self.listener.join()

    def __on_click(self, x: float, y: float, button: mouse.Button, pressed: bool) -> None:
        if button is mouse.Button.left:
            self.left_held = not self.left_held
        if button is mouse.Button.right:
            self.right_held = not self.right_held

    def __are_eyes_closed(self) -> bool:
        return self.right_held and self.left_held

    # TODO: Fix scaling issues
    def __on_move(self, x: float, y: float) -> None:
        if self.__are_eyes_closed():
            self.eyes_position_changed.emit(None, None)
            return

        screen_width, screen_height = get_screen_size()
        norm_x = x / screen_width
        norm_y = y / screen_height
        self.eyes_position_changed.emit(norm_x, norm_y)
