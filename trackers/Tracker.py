from visuals.GazeVisualizer import GazeVisualizer
from PyQt6.QtCore import QThread, pyqtSignal


class Tracker(QThread):
    eyes_position_changed: pyqtSignal = pyqtSignal(object, object)
    visualizer: GazeVisualizer | None = None

    def __init__(self, visualizer: GazeVisualizer | None = None) -> None:
        super().__init__()

        if visualizer:
            self.set_visualizer(visualizer)

    def set_visualizer(self, visualizer: GazeVisualizer | None) -> None:
        if not visualizer and self.visualizer:
            self.visualizer.movement_animation.stop()
            self.visualizer.deleteLater()

        self.visualizer = visualizer

        if visualizer:
            self.eyes_position_changed.connect(visualizer.set_position)
