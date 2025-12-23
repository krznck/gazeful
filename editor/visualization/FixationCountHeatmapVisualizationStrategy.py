from numpy.typing import NDArray
from editor.ParameterCollection import ParameterCollection
from editor.visualization.BaseHeatmapVisualizationStrategy import (
    BaseHeatmapVisualizationStrategy,
)
from processing.GazeStream import GazeStream
import numpy as np


class FixationCountHeatmapVisualizationStrategy(BaseHeatmapVisualizationStrategy):
    def __init__(self, parameters: ParameterCollection) -> None:
        super().__init__(parameters, "Amount of fixations")

    def _apply_fixation(
        self,
        heatmap: NDArray,
        row_indices: np.ndarray,
        column_indices: np.ndarray,
        fixation: GazeStream,
    ) -> None:
        _ = fixation
        heatmap[row_indices, column_indices] += 1
