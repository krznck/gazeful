"""Heatmap strategy based on the frequency of fixations at each location."""
import numpy as np
from numpy.typing import NDArray
from processing.GazeStream import GazeStream

from editor.ParameterCollection import ParameterCollection
from editor.visualization.BaseHeatmapVisualizationStrategy import \
    BaseHeatmapVisualizationStrategy


class FixationCountHeatmapVisualizationStrategy(BaseHeatmapVisualizationStrategy):
    """Generates a heatmap where intensity represents the number of fixations."""

    def __init__(self, parameters: ParameterCollection) -> None:
        """Initializes the fixation count heatmap strategy."""
        super().__init__(parameters, "Amount of fixations")

    def _apply_fixation(
        self,
        heatmap: NDArray,
        row_indices: np.ndarray,
        column_indices: np.ndarray,
        fixation: GazeStream,
    ) -> None:
        """Increments heatmap values by 1 for each fixation.

        Args:
            heatmap: The accumulation grid.
            row_indices: Row coordinates for the fixation area.
            column_indices: Column coordinates for the fixation area.
            fixation: The fixation data stream (unused).
        """
        _ = fixation
        heatmap[row_indices, column_indices] += 1
