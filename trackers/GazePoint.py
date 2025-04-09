from dataclasses import dataclass


@dataclass
class GazePoint:
    """Represents a basic unit of gaze.
    NOTE: Unrelated to Gazepoint brand eyetrackers."""

    x: float | None = None
    y: float | None = None
    timestamp: float = 0.0

    def are_eyes_closed(self):
        return self.x is None or self.y is None

    def are_eyes_open(self):
        return not self.are_eyes_closed()
