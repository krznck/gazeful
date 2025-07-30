from typing import Sequence

import numpy as np
from scipy.ndimage import gaussian_filter
from skimage.draw import disk

from processing.GazeStream import GazeStream
from visualizing.configuration.HeatmapConfiguration import HeatmapConfiguration
from visualizing.HeatmapStrategy import HeatmapStrategy


class AbsoluteGazeDurationHeatmapStrategy(HeatmapStrategy):
    def __init__(self, configuration: HeatmapConfiguration) -> None:
        super().__init__(
            configuration=configuration,
            title="Absolute Gaze Duration Heatmap",
            tick_label="sec",
        )

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
            heatmap[rr, cc] += fixation.duration()

        heatmap = gaussian_filter(heatmap, sigma=self.blur_power)
        return heatmap
