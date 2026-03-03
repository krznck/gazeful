"""Base visualization strategy interface and shared logic."""
from abc import ABC, ABCMeta, abstractmethod
from pathlib import Path

import numpy as np
from PIL import Image
from processing.algorithms.OculomotorAnalyzer import OculomotorAnalyzer
from processing.GazeRecording import GazeRecording
from processing.GazeStream import GazeStream
from PyQt6.QtCore import QObject, QRectF, pyqtSignal
from pyqtgraph import GraphicsLayoutWidget, ImageItem, PlotItem

from editor.ParameterCollection import ParameterCollection
from editor.parameters.base import ParameterEnum


class _VisualizationMeta(ABCMeta, type(QObject)):
    """Metaclass to resolve conflict between ABCMeta and QObject."""
    pass


class VisualizationStrategy(ABC, QObject, metaclass=_VisualizationMeta):
    """Abstract base class for all gaze visualization strategies.

    This class provides the foundation for different ways of visualizing gaze data 
    (e.g., Heatmaps, Gaze Plots). It handles the setup of the pyqtgraph plot, manages
    background images, and coordinates with parameter updates.

    Attributes:
        hovered: Signal emitted with a description string when a point is hovered.
        _plot: The main pyqtgraph PlotItem used for drawing.
        _parameters: Reference to the parameter collection for settings.
        _image_item: The background image item.
        _recording: The current gaze recording being visualized.
        _background_cache: Cached path to a background image.
        _fixations: List of extracted fixations from the recording.
    """

    _plot: PlotItem
    _parameters: ParameterCollection
    _image_item: ImageItem
    _recording: GazeRecording | None
    _background_cache: Path | None
    _fixations: list[GazeStream] | None

    hovered = pyqtSignal(str)

    def __init__(self, parameters: ParameterCollection) -> None:
        """Initializes the visualization strategy and connects common signals.

        Args:
            parameters: The parameter collection for configuration.
        """
        super().__init__()
        self._parameters = parameters
        self._plot = PlotItem()
        self._recording = None
        self._background_cache = None
        self._image_item = ImageItem()

        parameters.connect(ParameterEnum.OPACITY, self._opacity_updated)
        parameters.connect(ParameterEnum.FIX_MIN_DURATION, self._fix_info_updated)
        parameters.connect(ParameterEnum.FIX_MAX_DISPERSION, self._fix_info_updated)
        parameters.connect(ParameterEnum.BACKGROUND, self._background_updated)

    def setup_plot(
        self, graphics: GraphicsLayoutWidget, recording: GazeRecording
    ) -> None:
        """Configures the graphics widget for the current recording.

        Args:
            graphics: The layout widget to draw into.
            recording: The gaze data to visualize.
        """
        self._recording = recording

        if not recording.screenshot and (cache := self._background_cache):
            recording.screenshot = cache

        graphics.clear()  # type: ignore
        self._plot.clear()

        graphics.setBackground("white")

        plot = self._plot
        graphics.addItem(plot, row=1, col=0)  # type: ignore

        self._set_image()

    def _set_image(self) -> None:
        """Sets or refreshes the background image on the plot."""
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
        """Slot triggered when the background image path parameter is changed."""
        path = self._parameters.get_value(ParameterEnum.BACKGROUND)
        r = self._recording
        if r is None:
            self._background_cache = Path(path)
            return

        r.screenshot = Path(path)
        self._background_cache = r.screenshot
        self._set_image()

    def _fix_info_updated(self, _) -> None:
        """Slot triggered when fixation detection parameters are changed."""
        self.update()

    def _analyze(self, recording: GazeRecording) -> list[GazeStream]:
        """Runs the oculomotor analyzer to extract fixations.

        Args:
            recording: The recording to analyze.

        Returns:
            A list of extracted fixation streams.
        """
        fix_disp = self._parameters.get_value(ParameterEnum.FIX_MAX_DISPERSION)
        fix_dur = self._parameters.get_value(ParameterEnum.FIX_MIN_DURATION)
        analyzer = OculomotorAnalyzer(recording, fix_dur, fix_disp)
        self._fixations = analyzer.extract_fixations()

        return self._fixations

    @abstractmethod
    def _opacity_updated(self, _, value) -> None:
        """Abstract method to handle opacity changes for the visualization overlay."""
        pass

    @abstractmethod
    def update(self) -> None:
        """Abstract method to redraw the visualization based on current data/settings."""
        pass
