from typing import Final

from processing.GazeRecording import GazeRecording


class BaseAnalyzer:
    recording: Final[GazeRecording]

    def __init__(self, data: GazeRecording) -> None:
        self.recording = data
