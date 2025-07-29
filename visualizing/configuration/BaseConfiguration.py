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
    legend: Ref[bool]
    metadata: Ref[bool]

    def __init__(self, recording: GazeRecording | None = None) -> None:
        self._default()

        if recording:
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
        self.legend = Ref(True)
        self.metadata = Ref(True)
