from visuals.GazeVisualizer import get_screen_size
from PyQt6.QtGui import QCursor


class MouseTracker:
    def sample(self):
        screen_width, screen_height = get_screen_size()
        x = QCursor.pos().x()
        y = QCursor.pos().y()

        rel_x = x / screen_width
        rel_y = y / screen_height

        return rel_x, rel_y
