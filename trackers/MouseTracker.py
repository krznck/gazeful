from PyQt6.QtCore import QThread, pyqtSignal
from visuals.GazeVisualizer import get_screen_size
from visuals.GazeVisualizer import GazeVisualizer
from pynput import mouse
import atexit


# TODO: Potentially generalize trackers to reduce code duplication?
class MouseTracker(QThread):
    mouse_moved = pyqtSignal(float, float)
    visualizer: GazeVisualizer

    def __init__(self, visualizer: GazeVisualizer | None = None) -> None:
        super().__init__()
        self.listener = mouse.Listener(
            on_move=self.__on_move)
        atexit.register(self.__stop)

        if (visualizer is not None):
            self.set_visualizer(visualizer)

    def set_visualizer(self, visualizer: GazeVisualizer) -> None:
        self.visualizer = visualizer
        self.mouse_moved.connect(visualizer.set_position)

    def run(self):
        self.listener.start()
        self.listener.join()

    def __on_move(self, x, y):
        screen_width, screen_height = get_screen_size()
        norm_x = x / screen_width
        norm_y = y / screen_height
        self.mouse_moved.emit(norm_x, norm_y)

    def __stop(self):
        self.listener.stop()
        self.quit()
        self.wait()
