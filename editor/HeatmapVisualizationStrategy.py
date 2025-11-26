from PyQt6.QtCore import QRectF
import numpy as np
from pyqtgraph import colormap
from pyqtgraph.graphicsItems.ColorBarItem import ColorBarItem
from editor.HoverableImageItem import HoverableImageItem
from editor.ParameterCollection import ParameterCollection, ParameterEnum
from editor.VisualizationStrategy import VisualizationStrategy
from processing.GazeRecording import GazeRecording
from processing.algorithms2.OculomotorAnalyzer import OculomotorAnalyzer
from scipy.ndimage import gaussian_filter
from skimage.draw import disk


class HeatmapVisualizationStrategy(VisualizationStrategy):
    _heatmap_item: HoverableImageItem | None
    _colorbar: ColorBarItem | None

    def __init__(self, parameters: ParameterCollection) -> None:
        self._heatmap_item = None
        self._colorbar = None
        super().__init__(parameters)

    def setup_plot(self, recording: GazeRecording) -> None:
        super().setup_plot(recording)
        params = self._parameters
        opacity = params.get_value(ParameterEnum.OPACITY)

        self._heatmap_item = heatmap_item = HoverableImageItem()
        heatmap_item.setOpacity(opacity)
        heatmap_item.hovered.connect(self._on_hover)
        self._plot.addItem(heatmap_item)

        cmap = colormap.get(name="turbo")  # TODO: ditto
        self._colorbar = colorbar = ColorBarItem(
            colorMap=cmap,
            interactive=True,
            label="Seconds of fixation duration",
            orientation="horizontal",
        )
        colorbar.setImageItem(heatmap_item)
        self._graphics.addItem(colorbar, row=2, col=0)  # type: ignore

    def update(self):
        rec = self._recording
        heat_i = self._heatmap_item
        colorbar = self._colorbar
        if not rec or not heat_i or not colorbar:
            return

        fix_disp = self._parameters.get_value(ParameterEnum.FIX_MAX_DISPERSION)
        fix_dur = self._parameters.get_value(ParameterEnum.FIX_MIN_DURATION)
        analyzer = OculomotorAnalyzer(rec, fix_dur, fix_disp)

        fixations = analyzer.extract_fixations()

        sw, sh = rec.screen
        heatmap = np.zeros((sh, sw), dtype=np.float32)
        if fixations:
            radius = fix_disp / 2
            for fixation in fixations:
                cx, cy = fixation.centroid
                x = int(cx * sw)
                y = int(cy * sh)
                rr, cc = disk((y, x), radius, shape=heatmap.shape)
                heatmap[rr, cc] += fixation.duration()

        heatmap = gaussian_filter(heatmap, sigma=4)
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
