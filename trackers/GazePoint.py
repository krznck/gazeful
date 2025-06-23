from __future__ import annotations

from dataclasses import dataclass
from dataclasses import fields

# NOTE: __future__ allows us to annotate GazePoint in comparison logic,
# before the class is fully constructed


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
        if self.timestamp < 0.0:
            raise InvalidTimestampError(
                "Attempted to generate a gaze point with an invalid timestamp"
            )

    def are_eyes_closed(self):
        return self.x is None or self.y is None

    def are_eyes_open(self):
        return not self.are_eyes_closed()

    def compare_x(self, other: GazePoint) -> int:
        if self.x is None and other.x is None:
            return 0
        if self.x is None:
            return -1
        if other.x is None:
            return 1

        assert self.x is not None and other.x is not None
        return (self.x > other.x) - (self.x < other.x)

    def compare_y(self, other: GazePoint) -> int:
        if self.y is None and other.y is None:
            return 0
        if self.y is None:
            return -1
        if other.y is None:
            return 1

        assert self.y is not None and other.y is not None
        return (self.y > other.y) - (self.y < other.y)


def list_fields():
    return [f.name for f in fields(GazePoint)]
