from typing import Any
from editor.visualization.AbsoluteGazeDurationHeatmapVisualizationStrategy import (
    AbsoluteGazeDurationHeatmapVisualizationStrategy,
)
from editor.visualization.FixationCountHeatmapVisualizationStrategy import (
    FixationCountHeatmapVisualizationStrategy,
)
from editor.visualization.GazePlotVisualizationStrategy import (
    GazePlotVisualizationStrategy,
)
from editor.visualization.VisualizationKind import VisualizationKind
from editor.visualization.VisualizationStrategy import VisualizationStrategy
import editor.parameters.heatmap as heatmap
import editor.parameters.gaze_plot as gaze_plot

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
    match kind:
        case VisualizationKind():
            return STRAT_BY_KIND[kind]
        case str():
            for k in VisualizationKind:
                if k.value == kind:
                    return STRAT_BY_KIND[k]

    raise RuntimeError(f"Could not parse out visualization type - {kind}.")


def make_param(kind: str | VisualizationKind) -> list[dict[str, Any]]:
    match kind:
        case VisualizationKind():
            return PARAM_BY_KIND[kind]
        case str():
            for k in VisualizationKind:
                if k.value == kind:
                    return PARAM_BY_KIND[k]

    raise RuntimeError(f"Could not parse out visualization type - {kind}.")
