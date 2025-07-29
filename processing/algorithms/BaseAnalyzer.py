from typing import Final

from processing.Definitions import Definitions
from processing.GazeRecording import GazeRecording


class BaseAnalyzer:
    recording: Final[GazeRecording]
    defs: Final[Definitions]

    def __init__(self, data: GazeRecording, defs: Definitions) -> None:
        self.recording = data
        self.defs = defs
