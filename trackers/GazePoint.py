from dataclasses import dataclass


class InvalidTimestampError(Exception):
    """Raised when the GazePoint timestamp is not a valid time."""

    pass


@dataclass
class GazePoint:
    """Represents a basic unit of gaze.
    NOTE: Unrelated to Gazepoint brand eyetrackers."""

    x: float | None = None
    y: float | None = None
    timestamp: float = 0.0

    def __post_init__(self):
        if self.timestamp <= 0.0:
            raise InvalidTimestampError(
                "Attempted to generate a gaze point with an invalid timestamp"
            )

    def are_eyes_closed(self):
        return self.x is None or self.y is None

    def are_eyes_open(self):
        return not self.are_eyes_closed()
