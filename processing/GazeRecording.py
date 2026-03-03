"""Defines the GazeRecording class which bundles gaze data with metadata."""
from pathlib import Path
from typing import Final

from processing.GazeStream import GazeStream


class GazeRecording:
    """A container for a gaze data stream and its associated environment metadata.

    Attributes:
        data: The stream of captured GazePoints.
        screen: Dimensions (width, height) of the screen used during recording.
        screenshot: Path to a screenshot captured during the recording, if any.
    """

    def __init__(
        self,
        data: GazeStream,
        screen_dimensions: tuple[int, int],
        screenshot: Path | None = None,
    ) -> None:
        """Initializes a GazeRecording.

        Args:
            data: The stream of gaze data.
            screen_dimensions: The resolution of the tracked screen.
            screenshot: Optional path to an image of the screen.
        """
        self.data: Final[GazeStream] = data
        self.screen: Final[tuple[int, int]] = screen_dimensions
        self.screenshot: Path | None = screenshot

    def __len__(self) -> int:
        """Returns the number of points in the recording."""
        return len(self.data)
