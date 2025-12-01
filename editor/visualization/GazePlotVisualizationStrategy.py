from pyqtgraph import GraphicsLayoutWidget
from pyqtgraph.functions import mkBrush, mkPen
from pyqtgraph.graphicsItems.PlotDataItem import PlotDataItem
from pyqtgraph.graphicsItems.ScatterPlotItem import ScatterPlotItem
from pyqtgraph.graphicsItems.TextItem import TextItem
from editor.visualization.VisualizationStrategy import VisualizationStrategy
from editor.ParameterCollection import ParameterCollection, ParameterEnum
from processing.GazeRecording import GazeRecording


class GazePlotVisualizationStrategy(VisualizationStrategy):
    _fix_labels: list[TextItem]
    _connection_lines: list[PlotDataItem]
    _scatter: ScatterPlotItem

    def __init__(self, parameters: ParameterCollection) -> None:
        super().__init__(parameters)
        self._fix_labels = []
        self._connection_lines = []

        # FIXME: magic value
        self._scatter = ScatterPlotItem(size=10, brush=mkBrush("blue"))

    def setup_plot(
        self, graphics: GraphicsLayoutWidget, recording: GazeRecording
    ) -> None:
        super().setup_plot(graphics, recording)

    def _opacity_updated(self, _, value) -> None:
        return super()._opacity_updated(_, value)

    def update(self) -> None:
        super().update()
        rec = self._recording
        if not rec:
            return
        scatter = self._scatter
        cl = self._connection_lines
        plot = self._plot
        fl = self._fix_labels
        params = self._parameters

        scatter.clear()
        for line in cl:
            plot.removeItem(line)
        cl.clear()
        for item in fl:
            plot.removeItem(item)
        fl.clear()

        fixations = self._analyze(rec)

        fixation_spots = []
        path_cords = {"x": [], "y": []}
        sw, sh = rec.screen
        opacity = params.get_value(ParameterEnum.OPACITY)
        # c_color = self.parameters.param("Connection color").value()
        # h_color = self.parameters.param("Hover color").value()
        # aa = self.parameters.param("Antialiasing").value()

        for i, fix in enumerate(fixations):
            if fix.is_empty():
                continue

            duration = fix.duration()
            center_x, center_y = fix.centroid

            # need to normalize coordinates to screen dimensions
            pixel_x = center_x * sw
            pixel_y = center_y * sh

            # proportion size of the circles to fix duration, but also show shorties
            size = 10 + (duration * 50)

            fixation_spots.append(
                {
                    "pos": (pixel_x, pixel_y),
                    "size": size,
                    "data": {f"{i+1};{pixel_x};{pixel_y};{duration}"},
                }
            )

            path_cords["x"].append(pixel_x)
            path_cords["y"].append(pixel_y)

            label = TextItem(f"{i+1}", color="black", anchor=(0.5, 0.5))
            label.setPos(pixel_x, pixel_y)
            label.setOpacity(opacity)
            label.setZValue(10)
            plot.addItem(label)
            fl.append(label)

        x_coords = path_cords["x"]
        y_coords = path_cords["y"]
        for i in range(len(x_coords) - 1):
            line = plot.plot(
                [x_coords[i], x_coords[i + 1]],
                [y_coords[i], y_coords[i + 1]],
                pen=mkPen(color="blue", width=2),  # FIXME: magic value
                antialias=False,  # FIXME: magic bool (should be param)
            )
            line.setOpacity(opacity)
            cl.append(line)

        scatter.sigHovered.connect(self._on_hover)
        scatter.setOpacity(opacity)
        scatter.addPoints(
            spots=fixation_spots,
            antialias=False,  # FIXME: magic bool (should be param)
            hoverable=True,
            hoverSize=-1,
            hoverBrush="orange",  # FIXME: magic string
            pxMode=False,
            tip=None,
        )
        plot.addItem(scatter)

    # TODO: Implement in ABC in a sane way.
    # Though in the exploratory repo the two hover methods work differently with
    # different signatures, I think they could still be turned into the same
    # signature that just then emits/returns the information that the hover label
    # should have.
    def _on_hover(self):
        pass
