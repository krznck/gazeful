"""Base class for all gaze data analysis components."""
from typing import Final

from processing.GazeRecording import GazeRecording


class BaseAnalyzer:
    """Interface for components that perform calculations on GazeRecording data.

    Attributes:
        recording: The gaze recording data to analyze.
    """

    recording: Final[GazeRecording]

    def __init__(self, data: GazeRecording) -> None:
        """Initializes the analyzer with recording data.

        Args:
            data: The recording to be analyzed.
        """
        self.recording = data
