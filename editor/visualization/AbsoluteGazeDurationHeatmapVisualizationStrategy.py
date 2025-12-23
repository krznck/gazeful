from numpy.typing import NDArray
from editor.ParameterCollection import ParameterCollection
from editor.visualization.BaseHeatmapVisualizationStrategy import (
    BaseHeatmapVisualizationStrategy,
)
from processing.GazeStream import GazeStream
import numpy as np


class AbsoluteGazeDurationHeatmapVisualizationStrategy(
    BaseHeatmapVisualizationStrategy
):
    def __init__(self, parameters: ParameterCollection) -> None:
        super().__init__(parameters, "Seconds of fixation duration")

    def _apply_fixation(
        self,
        heatmap: NDArray,
        row_indices: np.ndarray,
        column_indices: np.ndarray,
        fixation: GazeStream,
    ) -> None:
        heatmap[row_indices, column_indices] += fixation.duration()
