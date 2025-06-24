from typing import Final

from processing.Definitions import Definitions
from processing.GazeStream import GazeStream


class BaseAnalyzer:
    main_stream: Final[GazeStream]
    defs: Final[Definitions]

    def __init__(self, data: GazeStream, defs: Definitions) -> None:
        self.main_stream = data
        self.defs = defs
