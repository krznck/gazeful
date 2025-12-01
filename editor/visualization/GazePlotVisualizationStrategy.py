from pyqtgraph import GraphicsLayoutWidget, PlotItem
from pyqtgraph.functions import mkBrush
from pyqtgraph.graphicsItems.PlotDataItem import PlotDataItem
from pyqtgraph.graphicsItems.ScatterPlotItem import ScatterPlotItem
from editor.visualization.VisualizationStrategy import VisualizationStrategy
from editor.ParameterCollection import ParameterCollection, ParameterEnum
from processing.GazeRecording import GazeRecording


class GazePlotVisualizationStrategy(VisualizationStrategy):
    def __init__(self, parameters: ParameterCollection) -> None:
        super().__init__(parameters)

    def setup_plot(
        self, graphics: GraphicsLayoutWidget, recording: GazeRecording
    ) -> None:
        super().setup_plot(graphics, recording)

    def _opacity_updated(self, _, value) -> None:
        return super()._opacity_updated(_, value)

    def update(self) -> None:
        return super().update()
