from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import QThread

from trackers.GazePoint import GazePoint
from visuals.visualizer.GazeVisualizer import GazeVisualizer


class TrackerNotConnectedError(Exception):
    """Raised when the physical tracker device is not connected to the computer."""

    pass


class Tracker(QThread):
    """
    Base eyetracker class that all concrete eyetrackers should inherit from.

    This class provides threading capabilities by inheriting from QThread,
    and contains an optional gaze visualizer. It emits a signal whenever new
    gaze data is received from the physical tracker device.

    Attributes:
        eyes_position_changed (pyqtSignal): Signal emitted when new gaze data is received.
            Signal emits:
                - a single point of data as represented by GazePoint

        visualizer (GazeVisualizer or None): Visualizer that follows eye movement.
    """

    eyes_position_changed: pyqtSignal = pyqtSignal(GazePoint)
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
