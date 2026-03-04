"""A subclass of the pyqtgraph ImageItem that reports hover positions."""

from PyQt6.QtCore import pyqtSignal
from pyqtgraph import ImageItem
from pyqtgraph.GraphicsScene.mouseEvents import HoverEvent
from pyqtgraph.Point import Point


class HoverableImageItem(ImageItem):
    """An ImageItem that emits a signal when the mouse hovers over it.

    Attributes:
        hovered: Signal emitted with the local coordinates of the hover event.
    """

    hovered = pyqtSignal(Point)

    def __init__(self, image=None, **kargs):
        """Initializes the hoverable image item and enables hover events."""
        super().__init__(image, **kargs)
        self.setAcceptHoverEvents(True)
        # WARNING:
        # We are not signaling when the hover event exits (ev.isExit()), which means
        # we can't stop displaying the information. Might be fine with what is planned

    def hoverEvent(self, ev: HoverEvent):
        """Handles the pyqtgraph hover event and emits the 'hovered' signal.

        Args:
            ev: The hover event.
        """
        if ev is None or ev.isExit():
            return

        pos = ev.pos()
        self.hovered.emit(pos)
