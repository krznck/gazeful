from abc import ABC
from dataclasses import dataclass
from pathlib import Path

from Ref import Ref


@dataclass
class BaseConfiguration(ABC):
    screen_width: Ref[int]
    screen_height: Ref[int]
    background_image: Ref[Path | None]
    opaqueness: Ref[float]

    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        background_image: Path | None = None,
        opagueness: float = 1.0,
    ) -> None:
        self.screen_width, self.screen_height = Ref(screen_width), Ref(screen_height)
        self.background_image = Ref(None)
        if background_image:
            self.background_image = Ref(background_image)
        self.opaqueness = Ref(opagueness)
        super().__init__()
