from abc import abstractmethod
from typing import Sequence

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from matplotlib.axes import Axes
from matplotlib.colors import ListedColormap
from matplotlib.figure import Figure

from processing.GazeStream import GazeStream
from visualizing.configuration.HeatmapConfiguration import HeatmapConfiguration
from visualizing.configuration.Metadata import Metadata
from visualizing.VisualizationStrategy import VisualizationStrategy


class HeatmapStrategy(VisualizationStrategy[HeatmapConfiguration]):
    def __init__(
        self,
        configuration: HeatmapConfiguration,
        title: str,
        tick_label: str,
    ) -> None:
        super().__init__(configuration)
        self.title = title
        self.colobar_tick_label = tick_label

    def visualize(
        self, data: Sequence[GazeStream], meta: Metadata
    ) -> tuple[Figure, Axes]:
        conf = self.configuration

        fig, ax = self._prepare_subplots()

        self._draw_background(ax)

        self._set_axes(ax, self.title)

        im = ax.imshow(
            X=self._generate_heatmap(data=data, max_disp=meta.max_fixation_dispersion),
            cmap=self._generate_colormap(),
            origin="lower",
            alpha=conf.opaqueness.value,
        )

        if conf.legend:
            cbar = fig.colorbar(
                mappable=im,
                ax=ax,
                shrink=0.5,
                pad=0.02,
            )
            vmin, vmax = im.get_clim()
            cbar.set_ticks([vmin, vmax])
            cbar.ax.yaxis.set_major_formatter(
                mticker.FuncFormatter(
                    lambda x, _: f"{int(x)} {self.colobar_tick_label}"
                )
            )

        if conf.metadata:
            self._set_metadata(fig, ax, meta)

        return fig, ax

    @abstractmethod
    def _generate_heatmap(
        self, data: Sequence[GazeStream], max_disp: float
    ) -> np.ndarray:
        pass

    def _generate_colormap(self) -> ListedColormap:
        # NOTE: This way, the heatmap starts off completely transparent at low values,
        # and sharply increases to being opaque
        cutoff = 0.05
        cmap = plt.get_cmap("hot")
        N = cmap.N
        colors = cmap(np.linspace(0, 1, N))
        x = np.linspace(0, 1, N)
        alpha = np.where(x <= cutoff, x / cutoff, 1.0)
        colors[:, 3] = alpha
        return ListedColormap(colors)
