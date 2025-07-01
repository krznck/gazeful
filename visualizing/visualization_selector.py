from enum import Enum

from visualizing.configuration.BaseConfiguration import BaseConfiguration
from visualizing.configuration.GazePlotConfiguration import GazePlotConfiguration
from visualizing.GazePlotStrategy import GazePlotStrategy
from visualizing.VisualizationStrategy import VisualizationStrategy
from visuals.visualization_configurations.BaseConfigurationEditor import (
    BaseConfigurationEditor,
)
from visuals.visualization_configurations.GazePlotConfigurationEditor import (
    GazePlotConfigurationEditor,
)


class VisualizationsEnum(Enum):
    PLOT = 0


def create_visualizer(
    vis_type: VisualizationsEnum | str,
) -> tuple[BaseConfiguration, VisualizationStrategy, BaseConfigurationEditor]:
    if isinstance(vis_type, str):
        vis_type = VisualizationsEnum[vis_type.upper()]

    match vis_type:
        case VisualizationsEnum.PLOT:
            conf = GazePlotConfiguration()
            return conf, GazePlotStrategy(conf), GazePlotConfigurationEditor(conf)
