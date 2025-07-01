from Ref import Ref
from visualizing.configuration.BaseConfiguration import BaseConfiguration


class GazePlotConfiguration(BaseConfiguration):
    size_multiplier: Ref[float]

    def __init__(
        self,
        screen_width: int = 1920,
        screen_height: int = 1080,
        size_multiplier: int = 500,
    ) -> None:
        self.size_multiplier = Ref(size_multiplier)
        super().__init__(screen_width, screen_height)
