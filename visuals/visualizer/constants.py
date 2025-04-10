from PyQt6.QtCore import QEasingCurve
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtGui import QPainter

TITLE = "Gaze Visualizer Window"
WIDTH = HEIGHT = 100
OPACITY = 153  # out of 255
WINDOW_FLAGS = (
    Qt.WindowType.Tool
    | Qt.WindowType.WindowStaysOnTopHint
    | Qt.WindowType.FramelessWindowHint
)
WIDGET_ATTRIBUTES: tuple = (
    Qt.WidgetAttribute.WA_TranslucentBackground,
    Qt.WidgetAttribute.WA_TransparentForMouseEvents,
)

RING_RENDER_HINT = QPainter.RenderHint.Antialiasing
RING_STYLE = Qt.PenStyle.SolidLine
RING_COLOR = QColor(255, 0, 0, OPACITY)  # red
RING_THICKNESS = 3
RING_MARGIN = 0.1

MOVEMENT_ANIMATION_EASING_CURVE = QEasingCurve.Type.Linear
MOVEMENT_ANIMATION_DURATION_FALLOFF = 25
# NOTE: all these below are in milliseconds
MIN_MOVEMENT_ANIMATION_DURATION = 50
MAX_MOVEMENT_ANIMATION_DURATION = 800

DEFAULT_FADE_ANIMATION_DURATION = 150

ENTRANCE_ANIMATION_EASING_CURVE = QEasingCurve.Type.InOutQuad
