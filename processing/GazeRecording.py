from pathlib import Path
from typing import Final

from processing.GazeStream import GazeStream


class GazeRecording:
    def __init__(
        self,
        data: GazeStream,
        screen_dimensions: tuple[int, int] | None = None,
        screenshot: Path | None = None,
    ) -> None:
        self.data: Final[GazeStream] = data
        self.screen: None | Final[tuple[int, int]] = screen_dimensions
        self.screenshot: Final[Path] | None = screenshot
