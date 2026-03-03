"""Base abstract classes and interfaces for all eyetracker implementations."""
from abc import ABC, ABCMeta, abstractmethod

from PyQt6.QtCore import QThread, pyqtSignal

from recording.Recorder import Recorder
from trackers.GazePoint import GazePoint
from visuals.visualizer.GazeVisualizer import GazeVisualizer


class _TrackerMeta(ABCMeta, type(QThread)):
    """Custom metaclass to resolve the metaclass conflict between ABCMeta and QThread.

    This metaclass exists solely to resolve the metaclass conflict between
    ABCMeta and QThread.
    """
    pass
    pass


class TrackerNotConnectedError(Exception):
    """Raised when the physical tracker device is not connected to the computer."""

    pass


class Tracker(ABC, QThread, metaclass=_TrackerMeta):
    """Base eyetracker class that all concrete eyetrackers should inherit from.

    This class provides threading capabilities by inheriting from QThread,
    and contains an optional gaze visualizer. It emits a signal whenever new
    gaze data is received from the physical tracker device.

    Attributes:
        eyes_position_changed: Signal emitted when new gaze data is received.
        visualizer: Visualizer that follows eye movement.
        recorder: Recorder that writes gaze data to a file.
    """

    eyes_position_changed: pyqtSignal = pyqtSignal(GazePoint)
    visualizer: GazeVisualizer

    def __init__(self, visualizer: GazeVisualizer, recorder: Recorder) -> None:
        """Initializes the base tracker.

        Args:
            visualizer: Visualizer that follows eye movement.
            recorder: Recorder that writes gaze data to a file.
        """
        super().__init__()

        self.visualizer = visualizer
        self.recorder = recorder
        self.eyes_position_changed.connect(self.visualizer.set_position)
        self.eyes_position_changed.connect(self.recorder.write)

    def track(self) -> None:
        """Starts the tracking thread."""
        self.start()

    def stop(self) -> None:
        """Stops the tracking thread and hides the visualizer."""
        self.visualizer.hide()  # hide it before dying
        self.quit()
        self.wait()

    @staticmethod
    @abstractmethod
    def connected() -> bool:
        """Checks if the physical tracker device is connected.

        Returns:
            True if the tracker is connected, False otherwise.
        """
        pass
