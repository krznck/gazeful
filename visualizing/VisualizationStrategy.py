from abc import ABC
from abc import abstractmethod
from typing import Generic
from typing import Sequence
from typing import TypeVar

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from processing.GazeStream import GazeStream
from visualizing.configuration.BaseConfiguration import BaseConfiguration

Configuration = TypeVar("Configuration", bound=BaseConfiguration)


plt.rcParams["font.family"] = "serif"


class VisualizationStrategy(ABC, Generic[Configuration]):
    configuration: Configuration

    def __init__(self, configuration: Configuration) -> None:
        self.configuration = configuration
        super().__init__()

    @abstractmethod
    def visualize(self, data: Sequence[GazeStream]) -> tuple[Figure, Axes]:
        pass
