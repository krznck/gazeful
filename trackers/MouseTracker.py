# from PyQt6.QtCore import QThread, pyqtSignal
from visuals.GazeVisualizer import get_screen_size
from visuals.GazeVisualizer import GazeVisualizer
from trackers.Tracker import Tracker
from pynput import mouse


class MouseTracker(Tracker):
    def __init__(self, visualizer: GazeVisualizer | None = None) -> None:
        super().__init__(visualizer)
        self.listener = mouse.Listener(
            on_move=self.__on_move)

    def run(self):
        self.listener.start()
        self.listener.join()

    # TODO: Fix scaling issues
    def __on_move(self, x, y):
        screen_width, screen_height = get_screen_size()
        norm_x = x / screen_width
        norm_y = y / screen_height
        self.eyes_position_changed.emit(norm_x, norm_y)
