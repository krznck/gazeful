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
from visualizing.configuration.Metadata import Metadata

Configuration = TypeVar("Configuration", bound=BaseConfiguration)


plt.rcParams["font.family"] = "serif"


class VisualizationStrategy(ABC, Generic[Configuration]):
    configuration: Configuration

    def __init__(self, configuration: Configuration) -> None:
        self.configuration = configuration
        super().__init__()

    @abstractmethod
    def visualize(
        self, data: Sequence[GazeStream], meta: Metadata
    ) -> tuple[Figure, Axes]:
        pass

    def _draw_background(self, axes: Axes):
        if self.configuration.background_image.value is None:
            return

        sw = self.configuration.screen_width.value
        sh = self.configuration.screen_height.value
        image = plt.imread(self.configuration.background_image.value)
        axes.imshow(image, extent=(0, sw, 0, sh))

    def _prepare_subplots(self) -> tuple[Figure, Axes]:
        figure, axes = plt.subplots(figsize=(10, 8), dpi=150)
        return figure, axes

    def _set_axes(self, axes: Axes, title: str) -> None:
        sw = self.configuration.screen_width.value
        sh = self.configuration.screen_height.value
        axes.set_xlim(0, sw)
        axes.set_ylim(0, sh)
        axes.set_aspect("equal", adjustable="box")
        axes.set_title(f"{title} ({sw}x{sh})")

        # coordinate ticks aren't all that relevant for these
        axes.set_xticks([])
        axes.set_yticks([])
