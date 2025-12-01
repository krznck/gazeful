from abc import abstractmethod
from PyQt6.QtCore import QRectF, QTimer
import numpy as np
from numpy.typing import NDArray
from pyqtgraph import GraphicsLayoutWidget, colormap
from pyqtgraph.graphicsItems.ColorBarItem import ColorBarItem
from editor.HoverableImageItem import HoverableImageItem
from editor.ParameterCollection import ParameterCollection
from editor.parameters.base import ParameterEnum
from editor.parameters.heatmap import HeatmapParameterEnum
from editor.visualization.VisualizationStrategy import VisualizationStrategy
from processing.GazeRecording import GazeRecording
from scipy.ndimage import gaussian_filter
from skimage.draw import disk

from processing.GazeStream import GazeStream


class BaseHeatmapVisualizationStrategy(VisualizationStrategy):
    _heatmap_item: HoverableImageItem
    _colorbar: ColorBarItem
    _heatmap: NDArray | None

    def __init__(self, parameters: ParameterCollection, cbar_label: str) -> None:
        self._heatmap = None
        self._heatmap_item = HoverableImageItem()
        cmap = colormap.get(name=parameters.get_value(HeatmapParameterEnum.C_MAP))
        self._colorbar = ColorBarItem(
            colorMap=cmap,
            interactive=True,
            label=cbar_label,
            orientation="horizontal",
        )
        super().__init__(parameters)

        parameters.connect(HeatmapParameterEnum.C_MAP, self._update_colormap)
        parameters.connect(HeatmapParameterEnum.BLUR, self._update_blur)

        self._pending_blur_value = parameters.get_value(HeatmapParameterEnum.BLUR)
        self._blur_debouncer = bd = QTimer(self)
        bd.setSingleShot(True)
        bd.setInterval(150)
        bd.timeout.connect(self._apply_blur_update)

    def setup_plot(
        self, graphics: GraphicsLayoutWidget, recording: GazeRecording
    ) -> None:
        super().setup_plot(graphics, recording)
        params = self._parameters
        opacity = params.get_value(ParameterEnum.OPACITY)

        hi = self._heatmap_item
        hi.setOpacity(opacity)
        hi.hovered.connect(self._on_hover)
        self._plot.addItem(hi)

        color = self._colorbar
        color.setImageItem(hi)
        graphics.addItem(color, row=2, col=0)  # type: ignore

    def _update_colormap(self, _, value):
        cmap = colormap.get(name=value)
        self._colorbar.setColorMap(cmap)

    def _apply_blur_update(self):
        v = self._pending_blur_value
        if v is None:
            return

        heatmap = gaussian_filter(self._heatmap, sigma=v)
        self._heatmap_item.setImage(heatmap.T)
        self._colorbar.setLevels(values=(np.nanmin(heatmap), np.nanmax(heatmap)))

    def _update_blur(self, _, value):
        self._pending_blur_value = value
        self._blur_debouncer.start()  # NOTE: this resets the timer on each call
        # making it work as a proper debouncer

    def update(self):
        rec = self._recording
        if not rec:
            return
        heat_i = self._heatmap_item
        colorbar = self._colorbar

        fixations = self._analyze(rec)

        sw, sh = rec.screen
        self._heatmap = np.zeros((sh, sw), dtype=np.float32)
        fix_disp = self._parameters.get_value(ParameterEnum.FIX_MAX_DISPERSION)
        if fixations:
            radius = fix_disp / 2
            for fixation in fixations:
                cx, cy = fixation.centroid
                x = int(cx * sw)
                y = int(cy * sh)
                rr, cc = disk((y, x), radius, shape=self._heatmap.shape)
                self._apply_fixation(self._heatmap, rr, cc, fixation)

        heatmap = gaussian_filter(
            self._heatmap, sigma=self._parameters.get_value(HeatmapParameterEnum.BLUR)
        )
        heat_i.setImage(heatmap.T)
        heat_i.setRect(QRectF(0, 0, sw, sh))
        colorbar.setLevels(values=(np.nanmin(heatmap), np.nanmax(heatmap)))

    @abstractmethod
    def _apply_fixation(
        self,
        heatmap: NDArray,
        row_indices: np.ndarray,
        column_indices: np.ndarray,
        fixation: GazeStream,
    ) -> None:
        pass

    def _opacity_updated(self, _, value) -> None:
        heat_i = self._heatmap_item
        if not heat_i:
            return

        heat_i.setOpacity(value)

    def _on_hover(self, pos):
        rec = self._recording
        if not rec:
            return

        sw, sh = rec.screen
        hover_x, hover_y = pos.x(), pos.y()

        radius = self._parameters.get_value(ParameterEnum.FIX_MAX_DISPERSION) / 2

        found_fixations = []
        # NOTE:
        # Weirdly not that time-consuming to iterate over these on the balatro sample;
        # still, I can't help but wonder if maybe a hashmap (with position being keys)
        # would be better for this?

        fixations = self._fixations
        if not fixations:
            fixations = self._analyze(rec)

        for fixation in fixations:
            fix_x_px = fixation.centroid[0] * sw
            fix_y_px = fixation.centroid[1] * sh

            distance_sq = (hover_x - fix_x_px) ** 2 + (hover_y - fix_y_px) ** 2
            if distance_sq <= radius**2:
                found_fixations.append(fixation)

        duration = count = 0
        for fix in found_fixations:
            fix: GazeStream
            duration += fix.duration()
            count += 1
        if found_fixations:
            text = (
                f"{count} fixations at x: {round(pos.x())} "
                f"and y: {round(pos.y())}, total duration of "
                f"{round(duration, 2)}s"
            )
            self.hovered.emit(text)
