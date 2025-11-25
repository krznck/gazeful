from abc import ABC, abstractmethod

from PIL import Image
from PyQt6.QtCore import QRectF
from pyqtgraph import GraphicsLayoutWidget, ImageItem, PlotItem

import numpy as np
from editor.ParameterCollection import ParameterCollection
from processing.GazeRecording import GazeRecording


class VisualizationStrategy(ABC):
    _plot = PlotItem | None
    _parameters: ParameterCollection
    _recording: GazeRecording | None

    def __init__(self, parameters: ParameterCollection) -> None:
        super().__init__()
        self._parameters = parameters

    def setup_plot(
        self, graphics: GraphicsLayoutWidget, recording: GazeRecording
    ) -> None:
        self._recording = recording
        graphics.clear()  # type: ignore

        graphics.setBackground("white")

        self.plot = plot = PlotItem()
        graphics.addItem(plot, row=1, col=0)  # type: ignore
        if view := plot.getViewBox():
            view.setAspectLocked(True)
            view.invertY(True)

        sw, sh = recording.screen
        if img_path := recording.screenshot:
            try:
                img_data = np.array(Image.open(img_path))
                img_data = np.transpose(img_data, (1, 0, 2))
                img_item = ImageItem(img_data)
                img_item.setRect(QRectF(0, 0, sw, sh))
                plot.addItem(img_item)
            except FileNotFoundError:
                print(f"Warning: Image file not found at {img_path}")

    @abstractmethod
    def update(self) -> None:
        pass
