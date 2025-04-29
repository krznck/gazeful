from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import QThread

from recording.Recorder import Recorder
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

        visualizer (GazeVisualizer): Visualizer that follows eye movement.
        recorder (Recorder): Recorder that writes gaze data to a file.
    """

    eyes_position_changed: pyqtSignal = pyqtSignal(GazePoint)
    visualizer: GazeVisualizer

    def __init__(self, visualizer: GazeVisualizer, recorder: Recorder) -> None:
        super().__init__()

        self.visualizer = visualizer
        self.recorder = recorder
        self.eyes_position_changed.connect(self.visualizer.set_position)
        self.eyes_position_changed.connect(self.recorder.write)

    def track(self) -> None:
        self.start()

    def stop(self) -> None:
        self.visualizer.hide()  # hide it before dying
        self.quit()
        self.wait()
