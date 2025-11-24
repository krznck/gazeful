from pyqtgraph import GraphicsLayoutWidget
from editor.VisualizationStrategy import VisualizationStrategy
from processing.GazeRecording import GazeRecording


class HeatmapVisualizationStrategy(VisualizationStrategy):
    def __init__(self) -> None:
        super().__init__()

    def setup_plot(
        self, graphics: GraphicsLayoutWidget, recording: GazeRecording
    ) -> None:
        return super().setup_plot(graphics, recording)
