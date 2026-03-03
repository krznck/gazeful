"""Factory functions for creating visualization strategies and parameters."""
from typing import Any

import editor.parameters.gaze_plot as gaze_plot
import editor.parameters.heatmap as heatmap
from editor.visualization.AbsoluteGazeDurationHeatmapVisualizationStrategy import \
    AbsoluteGazeDurationHeatmapVisualizationStrategy
from editor.visualization.FixationCountHeatmapVisualizationStrategy import \
    FixationCountHeatmapVisualizationStrategy
from editor.visualization.GazePlotVisualizationStrategy import \
    GazePlotVisualizationStrategy
from editor.visualization.VisualizationKind import VisualizationKind
from editor.visualization.VisualizationStrategy import VisualizationStrategy

STRAT_BY_KIND = {
    VisualizationKind.GAZE_PLOT: GazePlotVisualizationStrategy,
    VisualizationKind.ABS_FIX_DUR_HEAT: AbsoluteGazeDurationHeatmapVisualizationStrategy,
    VisualizationKind.FIX_COUNT_HEAT: FixationCountHeatmapVisualizationStrategy,
}

PARAM_BY_KIND = {
    VisualizationKind.GAZE_PLOT: gaze_plot.PARAMS,
    VisualizationKind.ABS_FIX_DUR_HEAT: heatmap.PARAMS,
    VisualizationKind.FIX_COUNT_HEAT: heatmap.PARAMS,
}


def make_strategy(kind: str | VisualizationKind) -> type[VisualizationStrategy]:
    """Factory to retrieve a strategy class based on a VisualizationKind.

    Args:
        kind: The kind of visualization requested.

    Returns:
        The class (not an instance) of the requested VisualizationStrategy.

    Raises:
        RuntimeError: If the kind cannot be parsed or matched.
    """
    match kind:
        case VisualizationKind():
            return STRAT_BY_KIND[kind]
        case str():
            for k in VisualizationKind:
                if k.value == kind:
                    return STRAT_BY_KIND[k]

    raise RuntimeError(f"Could not parse out visualization type - {kind}.")


def make_param(kind: str | VisualizationKind) -> list[dict[str, Any]]:
    """Factory to retrieve parameter definitions for a VisualizationKind.

    Args:
        kind: The kind of visualization requested.

    Returns:
        A list of parameter configuration dictionaries.

    Raises:
        RuntimeError: If the kind cannot be parsed or matched.
    """
    match kind:
        case VisualizationKind():
            return PARAM_BY_KIND[kind]
        case str():
            for k in VisualizationKind:
                if k.value == kind:
                    return PARAM_BY_KIND[k]

    raise RuntimeError(f"Could not parse out visualization type - {kind}.")
