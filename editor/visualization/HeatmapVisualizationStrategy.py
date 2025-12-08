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


class HeatmapVisualizationStrategy(VisualizationStrategy):
    _heatmap_item: HoverableImageItem
    _colorbar: ColorBarItem
    _heatmap: NDArray | None

    def __init__(self, parameters: ParameterCollection) -> None:
        self._heatmap = None
        self._heatmap_item = HoverableImageItem()
        cmap = colormap.get(name=parameters.get_value(HeatmapParameterEnum.C_MAP))
        self._colorbar = ColorBarItem(
            colorMap=cmap,
            interactive=True,
            label="Seconds of fixation duration",
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
                self._heatmap[rr, cc] += fixation.duration()

        heatmap = gaussian_filter(
            self._heatmap, sigma=self._parameters.get_value(HeatmapParameterEnum.BLUR)
        )
        heat_i.setImage(heatmap.T)
        heat_i.setRect(QRectF(0, 0, sw, sh))
        colorbar.setLevels(values=(np.nanmin(heatmap), np.nanmax(heatmap)))

    def _opacity_updated(self, _, value) -> None:
        heat_i = self._heatmap_item
        if not heat_i:
            return

        heat_i.setOpacity(value)

    # TODO: Implement in ABC in a sane way.
    # Though in the exploratory repo the two hover methods work differently with
    # different signatures, I think they could still be turned into the same
    # signature that just then emits/returns the information that the hover label
    # should have.
    def _on_hover(self):
        pass
