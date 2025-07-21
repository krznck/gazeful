from enum import Enum

from processing.GazeRecording import GazeRecording
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
    PLOT = GazePlotStrategy


def create_visualizer(
    vis_type: VisualizationsEnum | str, recording: GazeRecording
) -> tuple[BaseConfiguration, VisualizationStrategy, BaseConfigurationEditor]:
    if isinstance(vis_type, str):
        vis_type = VisualizationsEnum[vis_type.upper()]

    match vis_type:
        case VisualizationsEnum.PLOT:
            conf = GazePlotConfiguration(recording)
            return conf, GazePlotStrategy(conf), GazePlotConfigurationEditor(conf)
