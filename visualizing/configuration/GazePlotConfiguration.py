from processing.GazeRecording import GazeRecording
from Ref import Ref
from visualizing.configuration.BaseConfiguration import BaseConfiguration


class GazePlotConfiguration(BaseConfiguration):
    size_multiplier: Ref[float]

    def __init__(
        self,
        recording: GazeRecording | None,
        size_multiplier: int = 300,
    ) -> None:
        self.size_multiplier = Ref(size_multiplier)
        super().__init__(recording)
