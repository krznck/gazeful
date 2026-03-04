"""Defines the GazePoint dataclass and related exceptions for gaze data."""

from __future__ import annotations

from dataclasses import dataclass, fields

# NOTE: __future__ allows us to annotate GazePoint in comparison logic,
# before the class is fully constructed


class InvalidTimestampError(Exception):
    """Raised when the GazePoint timestamp is not a valid time."""

    pass


@dataclass
class GazePoint:
    """Represents a basic unit of gaze.

    NOTE: Unrelated to Gazepoint brand eye trackers.

    Attributes:
        x: Normalized x coordinate (0.0 to 1.0) or None if eyes are closed.
        y: Normalized y coordinate (0.0 to 1.0) or None if eyes are closed.
        timestamp: Monotonic timestamp of the gaze capture.
    """

    x: float | None = None
    y: float | None = None
    timestamp: float = 0.0

    def __post_init__(self):
        """Validates the timestamp after initialization.

        Raises:
            InvalidTimestampError: If the timestamp is negative.
        """
        if self.timestamp < 0.0:
            raise InvalidTimestampError(
                "Attempted to generate a gaze point with an invalid timestamp"
            )

    def are_eyes_closed(self) -> bool:
        """Checks if both eye coordinates are missing.

        Returns:
            True if either x or y is None.
        """
        return self.x is None or self.y is None

    def are_eyes_open(self) -> bool:
        """Checks if both eye coordinates are present.

        Returns:
            True if both x and y are not None.
        """
        return not self.are_eyes_closed()

    def compare_x(self, other: GazePoint) -> int:
        """Compares the x coordinate with another GazePoint.

        Args:
            other: The other GazePoint to compare against.

        Returns:
            An integer indicating comparison result (-1, 0, 1).
        """
        if self.x is None and other.x is None:
            return 0
        if self.x is None:
            return -1
        if other.x is None:
            return 1

        assert self.x is not None and other.x is not None
        return (self.x > other.x) - (self.x < other.x)

    def compare_y(self, other: GazePoint) -> int:
        """Compares the y coordinate with another GazePoint.

        Args:
            other: The other GazePoint to compare against.

        Returns:
            An integer indicating comparison result (-1, 0, 1).
        """
        if self.y is None and other.y is None:
            return 0
        if self.y is None:
            return -1
        if other.y is None:
            return 1

        assert self.y is not None and other.y is not None
        return (self.y > other.y) - (self.y < other.y)


def list_fields() -> list[str]:
    """Lists the field names of the GazePoint dataclass.

    Returns:
        A list of strings representing the field names.
    """
    return [f.name for f in fields(GazePoint)]
