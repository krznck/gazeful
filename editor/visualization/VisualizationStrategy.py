from abc import ABC, ABCMeta, abstractmethod

from PIL import Image
from PyQt6.QtCore import QObject, QRectF
from pyqtgraph import GraphicsLayoutWidget, ImageItem, PlotItem

import numpy as np
from editor.ParameterCollection import ParameterCollection
from editor.parameters.base import ParameterEnum
from processing.GazeRecording import GazeRecording
from pathlib import Path

from processing.GazeStream import GazeStream
from processing.algorithms2.OculomotorAnalyzer import OculomotorAnalyzer


class _VisualizationMeta(ABCMeta, type(QObject)):
    pass


class VisualizationStrategy(ABC, QObject, metaclass=_VisualizationMeta):
    """
    Acts as a Model class for the Editor - handles all the logic in creating an
    interactable visualization, which is available via the `graphics` property.
    As it is a Strategy pattern, the model is interchangeable depending on which
    visualization is needed.
    This class is abstract and should not be instantiated directly.
    """

    _plot: PlotItem
    _parameters: ParameterCollection
    _image_item: ImageItem
    _recording: GazeRecording | None
    _background_cache: Path | None

    def __init__(self, parameters: ParameterCollection) -> None:
        super().__init__()
        self._parameters = parameters
        self._plot = PlotItem()
        self._recording = None
        self._background_cache = None
        self._image_item = ImageItem()

        # TODO: connect these for the specific enum values in specific strategies
        # (gaze plot opacity, the fixation and stuff color changes)

        parameters.connect(ParameterEnum.OPACITY, self._opacity_updated)
        parameters.connect(ParameterEnum.FIX_MIN_DURATION, self._fix_info_updated)
        parameters.connect(ParameterEnum.FIX_MAX_DISPERSION, self._fix_info_updated)
        parameters.connect(ParameterEnum.BACKGROUND, self._background_updated)

    def setup_plot(
        self, graphics: GraphicsLayoutWidget, recording: GazeRecording
    ) -> None:
        self._recording = recording
        graphics.clear()  # type: ignore
        self._plot.clear()

        graphics.setBackground("white")

        plot = self._plot
        graphics.addItem(plot, row=1, col=0)  # type: ignore

        self._set_image()

    def _set_image(self) -> None:
        recording = self._recording
        if not recording:
            return

        plot = self._plot
        if view := plot.getViewBox():
            view.setAspectLocked(True)
            view.invertY(True)
        img_item = self._image_item
        plot.removeItem(img_item)

        sw, sh = recording.screen
        if img_path := (recording.screenshot or self._background_cache):
            try:
                img_data = np.array(Image.open(img_path))
                img_data = np.transpose(img_data, (1, 0, 2))
                img_item.setImage(img_data)
                img_item.setRect(QRectF(0, 0, sw, sh))
                img_item.setZValue(-100)
                plot.addItem(img_item)
            except FileNotFoundError:
                print(f"Warning: Image file not found at {img_path}")

    def _background_updated(self, _) -> None:
        path = self._parameters.get_value(ParameterEnum.BACKGROUND)
        r = self._recording
        if r is None:
            self._background_cache = Path(path)
            return

        r.screenshot = Path(path)
        self._background_cache = r.screenshot
        self._set_image()

    def _fix_info_updated(self, _) -> None:
        self.update()

    def _analyze(self, recording: GazeRecording) -> list[GazeStream]:
        fix_disp = self._parameters.get_value(ParameterEnum.FIX_MAX_DISPERSION)
        fix_dur = self._parameters.get_value(ParameterEnum.FIX_MIN_DURATION)
        analyzer = OculomotorAnalyzer(recording, fix_dur, fix_disp)

        return analyzer.extract_fixations()

    @abstractmethod
    def _opacity_updated(self, _, value) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass
