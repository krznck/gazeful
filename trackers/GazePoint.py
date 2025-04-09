from dataclasses import dataclass


@dataclass
class GazePoint:
    """Represents a basic unit of gaze.
    NOTE: Unrelated to Gazepoint brand eyetrackers."""

    x: float | None = None
    y: float | None = None
    timestamp: float = 0.0
