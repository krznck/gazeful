from typing import Sequence

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.colors import ListedColormap
from matplotlib.figure import Figure
from scipy.ndimage import gaussian_filter

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
            X=self._generate_heatmap(data),
            cmap=self._generate_colormap(),
            origin="lower",
            alpha=conf.opaqueness.value,
        )
        # fig.colorbar(mappable=im, ax=ax, label="Fixation Overlap Count")

        return fig, ax

    def _generate_heatmap(self, data: Sequence[GazeStream]) -> np.ndarray:
        sh = self.configuration.screen_height.value
        sw = self.configuration.screen_width.value
        heatmap = np.zeros((sh, sw), dtype=np.float32)

        for fixation in data:
            disp = fixation.dispersion()
            cent = fixation.centroid()

            center_x = int(cent[0] * sw)
            center_y = int(sh - cent[1] * sh)
            radius = int(disp * sw)

            y, x = np.ogrid[-center_y : sh - center_y, -center_x : sw - center_x]
            mask = x * x + y * y <= radius * radius

            heatmap[mask] += 1

        heatmap = gaussian_filter(heatmap, sigma=2.0)
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
