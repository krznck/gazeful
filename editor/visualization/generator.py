from enum import Enum
from editor.visualization.HeatmapVisualizationStrategy import (
    HeatmapVisualizationStrategy,
)
from editor.visualization.GazePlotVisualizationStrategy import (
    GazePlotVisualizationStrategy,
)
from editor.visualization.VisualizationKind import VisualizationKind
from visualizing.VisualizationStrategy import VisualizationStrategy


STRAT_BY_KIND = {
    VisualizationKind.GAZE_PLOT: GazePlotVisualizationStrategy,
    VisualizationKind.ABS_FIX_DUR_HEAT: HeatmapVisualizationStrategy,
}


def make_strategy(kind: str | VisualizationKind) -> VisualizationStrategy:
    match kind:
        case VisualizationKind():
            return STRAT_BY_KIND[kind]
        case str():
            for k in VisualizationKind:
                if k.value == kind:
                    return STRAT_BY_KIND[k]

    raise RuntimeError(f"Could not parse out strategy - {kind}.")
