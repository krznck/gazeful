from enum import Enum

from visualizing.GazePlotStrategy import GazePlotStrategy
from visualizing.VisualizationStrategy import VisualizationStrategy


class VisualizationsEnum(Enum):
    PLOT = 0


def create_visualizer(vis_type: VisualizationsEnum | str) -> VisualizationStrategy:
    if isinstance(vis_type, str):
        vis_type = VisualizationsEnum[vis_type.upper()]

    match vis_type:
        case VisualizationsEnum.PLOT:
            return GazePlotStrategy()
