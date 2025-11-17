from PyQt6.QtCore import pyqtSignal
from pyqtgraph import ImageItem
from pyqtgraph.Point import Point


class HoverableImageItem(ImageItem):
    hovered = pyqtSignal(Point)

    def __init__(self, image=None, **kargs):
        super().__init__(image, **kargs)
        self.setAcceptHoverEvents(True)
        # WARNING:
        # We are not signaling when the hover event exits (ev.isExit()), which means
        # we can't stop displaying the information. Might be fine with what is planned

    def hoverEvent(self, ev):
        if ev is None:
            return

        pos = ev.pos()
        pos: Point
        # print(pos.x(), pos.y())
        self.hovered.emit(pos)
