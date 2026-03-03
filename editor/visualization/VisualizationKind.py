"""Enumeration of all supported visualization types."""
from enum import Enum


class VisualizationKind(Enum):
    """Types of visualizations that the editor can generate."""

    ABS_FIX_DUR_HEAT = "Absolute fixation duration heatmap"
    FIX_COUNT_HEAT = "Fixation count heatmap"
    GAZE_PLOT = "Gaze plot"
