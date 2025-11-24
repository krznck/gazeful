from abc import ABC

from PIL import Image
from PyQt6.QtCore import QRectF
from pyqtgraph import GraphicsLayoutWidget, ImageItem, PlotItem

import numpy as np
from processing.GazeRecording import GazeRecording


class VisualizationStrategy(ABC):
    def __init__(self) -> None:
        super().__init__()

    def setup_plot(
        self, graphics: GraphicsLayoutWidget, recording: GazeRecording
    ) -> None:
        graphics.clear()  # type: ignore

        graphics.setBackground("white")

        plot = PlotItem()
        graphics.addItem(plot, row=1, col=1)  # type: ignore
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
