from abc import ABC
from abc import abstractmethod
from typing import Sequence

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from processing.GazeStream import GazeStream


class VisualizationStrategy(ABC):
    @abstractmethod
    def visualize(self, data: Sequence[GazeStream]) -> tuple[Figure, Axes]:
        pass
