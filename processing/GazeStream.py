from __future__ import annotations

from trackers.GazePoint import GazePoint


class NonMonotonicTimesstampError(Exception):
    """Raised when a GazePoint with a non-monotonic timestamp is added."""


class GazeStream:
    points: list[GazePoint]

    def __init__(self, data: list[GazePoint] | None = None) -> None:
        self.points = []
        if data is not None:
            self.points = data

    def copy(self) -> GazeStream:
        return GazeStream(self.points.copy())

    def add(self, point: GazePoint) -> None:
        if self.length() == 0:
            self.points.append(point)
            return

        last = self.points[-1].timestamp
        if point.timestamp < last:
            raise NonMonotonicTimesstampError(
                f"Tried to add point with timestamp {point.timestamp} after {last}"
            )

        self.points.append(point)

    def pop_first(self) -> GazePoint:
        return self.points.pop(0)

    def get_duration(self) -> float:
        if (self.length()) == 1:
            return self.points[0].timestamp
        elif (self.length()) == 0:
            return 0
        else:
            return self.points[-1].timestamp - self.points[0].timestamp

    def is_empty(self) -> bool:
        return self.length() <= 0

    def length(self) -> int:
        return len(self.points)

    def clear(self) -> None:
        self.points.clear()

    def extremes(self) -> tuple[float, float, float, float]:
        xs = [p.x for p in self.points if p.x is not None]
        ys = [p.y for p in self.points if p.y is not None]

        if not xs or not ys:
            raise ValueError("No valid points to compute extremes")

        return max(xs), max(ys), min(xs), min(ys)

    def dispersion(self) -> float:
        max_x, max_y, min_x, min_y = self.extremes()
        return (max_x - min_x) + (max_y - min_y)

    def __str__(self) -> str:
        builder = f"--- {self.get_duration()*1000}ms fixation ---"
        for point in self.points:
            builder += "\n" + str(point)
        return builder
