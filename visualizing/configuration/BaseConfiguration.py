from abc import ABC
from dataclasses import dataclass

from Ref import Ref


@dataclass
class BaseConfiguration(ABC):
    screen_width: Ref[int]
    screen_height: Ref[int]

    def __init__(self, screen_width: int, screen_height: int) -> None:
        self.screen_width, self.screen_height = Ref(screen_width), Ref(screen_height)
        super().__init__()
