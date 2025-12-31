from pyqtgraph import GraphicsLayoutWidget, SpotItem, mkColor
from pyqtgraph.functions import mkBrush, mkPen
from pyqtgraph.graphicsItems.PlotDataItem import PlotDataItem
from pyqtgraph.graphicsItems.ScatterPlotItem import ScatterPlotItem
from pyqtgraph.graphicsItems.TextItem import TextItem
from editor.parameters.base import ParameterEnum
from editor.parameters.gaze_plot import GazePlotParameterEnum
from editor.visualization.VisualizationStrategy import VisualizationStrategy
from editor.ParameterCollection import ParameterCollection
from processing.GazeRecording import GazeRecording
import numpy as np


class GazePlotVisualizationStrategy(VisualizationStrategy):
    _fix_labels: list[TextItem]
    _connection_lines: list[PlotDataItem]
    _scatter: ScatterPlotItem

    def __init__(self, parameters: ParameterCollection) -> None:
        super().__init__(parameters)
        self._fix_labels = []
        self._connection_lines = []
        self._currently_hovered_spots = []
        self.HOVER_MULT = 1.5

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
        self._plot.addItem(self._scatter)

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
        for spot in self._scatter.points():
            spot.setBrush(value)

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

    def _on_hover(self, scatter: ScatterPlotItem, hovered: np.ndarray):
        params = self._parameters
        fix_color = params.get_value(GazePlotParameterEnum.FIX_COLOR)
        adj_color = params.get_value(GazePlotParameterEnum.ADJ_COLOR)
        con_color = params.get_value(GazePlotParameterEnum.CON_COLOR)
        last: set[SpotItem] = set(self._currently_hovered_spots)
        current: set[SpotItem] = set(hovered)
        info_text = ""

        for spot in last - current:
            spot.setSize(spot.size() / self.HOVER_MULT)
            prev, next = spot.index() - 1, spot.index() + 1
            all: list[SpotItem] = list(scatter.points())
            if prev >= 0:
                self._connection_lines[prev].setPen(con_color, width=2)
                prev = all[prev]
                prev.setBrush(fix_color)
            if next < len(all):
                self._connection_lines[next - 1].setPen(con_color, width=2)
                next = all[next]
                next.setBrush(fix_color)

        for spot in current - last:
            spot.setSize(spot.size() * self.HOVER_MULT)
            prev, next = spot.index() - 1, spot.index() + 1
            all: list[SpotItem] = list(scatter.points())
            if prev >= 0:
                self._connection_lines[prev].setPen(adj_color, width=4)
                prev = all[prev]
                prev.setBrush(adj_color)
            if next < len(all):
                self._connection_lines[next - 1].setPen(adj_color, width=4)
                next = all[next]
                next.setBrush(adj_color)

        point = ""
        duration = xs = ys = 0
        for spot in current:
            spot: SpotItem
            for data in spot.data():
                data = data.split(";")
                point += f"{data[0]}, "
                pos = spot.pos()
                xs += pos.x()
                ys += pos.y()
                duration += float(data[-1])

        if current:
            info_text = (
                f"Points {point}"
                f"around x:{round(xs/len(current))} "
                f"and y:{round(ys/len(current))} "
                f"total duration of {round(duration, 2)}s"
            )

        if len(current) > 0:
            self.hovered.emit(info_text)

        self._currently_hovered_spots = hovered
