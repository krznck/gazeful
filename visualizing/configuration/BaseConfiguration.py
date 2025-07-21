from abc import ABC
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from processing.GazeRecording import GazeRecording
from Ref import Ref


class DpiQualities(Enum):
    LOW = 100
    MEDIUM = 300
    HIGH = 600


@dataclass
class BaseConfiguration(ABC):
    screen_width: Ref[int]
    screen_height: Ref[int]
    background_image: Ref[Path | None]
    opaqueness: Ref[float]
    dpi: Ref[int]

    # def __init__(
    #     self,
    #     screen_width: int = 1920,
    #     screen_height: int = 1080,
    #     background_image: Path | None = None,
    #     opagueness: float = 1.0,
    #     dpi: int = DpiQualities.MEDIUM.value,
    # ) -> None:
    #     self.screen_width, self.screen_height = Ref(screen_width), Ref(screen_height)
    #     self.background_image = Ref(None)
    #     if background_image:
    #         self.background_image = Ref(background_image)
    #     self.opaqueness = Ref(opagueness)
    #     self.dpi = Ref(dpi)
    #     super().__init__()

    def __init__(self, recording: GazeRecording | None) -> None:
        self._default()

        if recording:
            if recording.screen:
                self.screen_width = Ref(recording.screen[0])
                self.screen_height = Ref(recording.screen[1])

            if recording.screenshot:
                self.background_image = Ref(recording.screenshot)

        super().__init__()

    def _default(self) -> None:
        self.screen_width, self.screen_height = Ref(1920), Ref(1080)
        self.background_image = Ref(None)
        self.opaqueness = Ref(1.0)
        self.dpi = Ref(DpiQualities.MEDIUM.value)
