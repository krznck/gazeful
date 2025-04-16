from dataclasses import dataclass


class InvalidTimestampError(Exception):
    """Raised when the GazePoint timestamp is not a valid time."""

    pass


EYE_CLOSED: str = "-"


@dataclass
class GazePoint:
    """Represents a basic unit of gaze.
    NOTE: Unrelated to Gazepoint brand eyetrackers."""

    x: float | None = None
    y: float | None = None
    timestamp: float = 0.0

    def __post_init__(self):
        if self.timestamp < 0.0:
            raise InvalidTimestampError(
                "Attempted to generate a gaze point with an invalid timestamp"
            )

    def are_eyes_closed(self):
        return self.x is None or self.y is None

    def are_eyes_open(self):
        return not self.are_eyes_closed()

    def __str__(self) -> str:
        x_str = self.x if self.x is not None else EYE_CLOSED
        y_str = self.y if self.y is not None else EYE_CLOSED
        return f"{x_str};{y_str};{self.timestamp}"
