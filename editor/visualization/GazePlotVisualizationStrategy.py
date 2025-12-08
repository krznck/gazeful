from pyqtgraph import GraphicsLayoutWidget, mkColor
from pyqtgraph.functions import mkBrush, mkPen
from pyqtgraph.graphicsItems.PlotDataItem import PlotDataItem
from pyqtgraph.graphicsItems.ScatterPlotItem import ScatterPlotItem
from pyqtgraph.graphicsItems.TextItem import TextItem
from editor.parameters.base import ParameterEnum
from editor.parameters.gaze_plot import GazePlotParameterEnum
from editor.visualization.VisualizationStrategy import VisualizationStrategy
from editor.ParameterCollection import ParameterCollection
from processing.GazeRecording import GazeRecording


class GazePlotVisualizationStrategy(VisualizationStrategy):
    _fix_labels: list[TextItem]
    _connection_lines: list[PlotDataItem]
    _scatter: ScatterPlotItem

    def __init__(self, parameters: ParameterCollection) -> None:
        super().__init__(parameters)
        self._fix_labels = []
        self._connection_lines = []

        self._scatter = ScatterPlotItem(
            size=10,
            brush=mkBrush(self._parameters.get_value(GazePlotParameterEnum.FIX_COLOR)),
        )

        parameters.connect(GazePlotParameterEnum.HOV_COLOR, self._update_hover_color)
        parameters.connect(
            GazePlotParameterEnum.CON_COLOR, self._update_connection_color
        )
        parameters.connect(GazePlotParameterEnum.FIX_COLOR, self._update_fix_color)
        parameters.connect(GazePlotParameterEnum.ANTIALIAS, self.update)

    def setup_plot(
        self, graphics: GraphicsLayoutWidget, recording: GazeRecording
    ) -> None:
        super().setup_plot(graphics, recording)

    def _opacity_updated(self, _, value) -> None:
        self._scatter.setOpacity(value)
        for line in self._connection_lines:
            line.setOpacity(value)
        for label in self._fix_labels:
            label.setOpacity(value)

    def _update_hover_color(self, _, value):
        # maniuplating the `opts` dictionary directly when there is no setter
        self._scatter.opts["hoverBrush"] = mkColor(value)

    def _update_fix_color(self, _, value):
        self._scatter.setBrush(value)

    def _update_connection_color(self, _, value):
        for line in self._connection_lines:
            line.setPen(color=value, width=2)

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
                pen=mkPen(
                    color=params.get_value(GazePlotParameterEnum.CON_COLOR), width=2
                ),
                antialias=params.get_value(GazePlotParameterEnum.ANTIALIAS),
            )
            line.setOpacity(opacity)
            cl.append(line)

        scatter.sigHovered.connect(self._on_hover)
        scatter.setOpacity(opacity)
        scatter.addPoints(
            spots=fixation_spots,
            antialias=params.get_value(GazePlotParameterEnum.ANTIALIAS),
            hoverable=True,
            hoverSize=-1,
            hoverBrush=params.get_value(GazePlotParameterEnum.HOV_COLOR),
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
