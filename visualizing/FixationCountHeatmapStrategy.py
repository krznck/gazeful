from typing import Sequence

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from matplotlib.axes import Axes
from matplotlib.colors import ListedColormap
from matplotlib.figure import Figure
from scipy.ndimage import gaussian_filter
from skimage.draw import disk

from processing.GazeStream import GazeStream
from visualizing.configuration.FixationCountHeatmapConfiguration import (
    FixationCountHeatmapConfiguration,
)
from visualizing.configuration.Metadata import Metadata
from visualizing.VisualizationStrategy import VisualizationStrategy


class FixationCountHeatmapStrategy(
    VisualizationStrategy[FixationCountHeatmapConfiguration]
):
    def __init__(self, configuration: FixationCountHeatmapConfiguration) -> None:
        super().__init__(configuration)

    def visualize(
        self, data: Sequence[GazeStream], meta: Metadata
    ) -> tuple[Figure, Axes]:
        conf = self.configuration

        fig, ax = self._prepare_subplots()

        self._draw_background(ax)

        self._set_axes(ax, "Fixation Count Heatmap")

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
                mticker.FuncFormatter(lambda x, _: f"{int(x)} fixations")
            )

        if conf.metadata:
            self._set_metadata(fig, ax, meta)

        return fig, ax

    def _generate_heatmap(
        self, data: Sequence[GazeStream], max_disp: float
    ) -> np.ndarray:
        sh = self.configuration.screen_height.value
        sw = self.configuration.screen_width.value
        heatmap = np.zeros((sh, sw), dtype=np.float32)
        radius = max_disp / 2  # we want the max dispersion to be the diamater

        for fixation in data:
            cx, cy = fixation.centroid
            x = int(cx * sw)
            y = sh - int(cy * sh)
            rr, cc = disk((y, x), radius, shape=heatmap.shape)
            heatmap[rr, cc] += 1

        heatmap = gaussian_filter(heatmap, sigma=5.0)
        return heatmap

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
