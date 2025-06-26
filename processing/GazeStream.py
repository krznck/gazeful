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

    def __iter__(self):
        return iter(self.points)

    def __len__(self) -> int:
        return len(self.points)

    def __getitem__(self, index: int) -> GazePoint:
        return self.points[index]

    def __str__(self) -> str:
        builder = f"--- {self.duration()*1000}ms fixation ---"
        for point in self:
            builder += f"\n {point}"
        return builder

    def copy(self) -> GazeStream:
        return GazeStream(self.points.copy())

    def append(self, point: GazePoint) -> None:
        if len(self) == 0:
            self.points.append(point)
            return

        last = self[-1].timestamp
        if point.timestamp < last:
            raise NonMonotonicTimesstampError(
                f"Tried to add point with timestamp {point.timestamp} after {last}"
            )

        self.points.append(point)

    def pop(self, index: int = -1) -> GazePoint:
        return self.points.pop(index)

    def duration(self) -> float:
        if (len(self)) == 1:
            return self[0].timestamp
        elif (len(self)) == 0:
            return 0
        else:
            return self[-1].timestamp - self[0].timestamp

    def is_empty(self) -> bool:
        return len(self) <= 0

    def clear(self) -> None:
        self.points.clear()

    def extremes(self) -> tuple[float, float, float, float]:
        xs = [p.x for p in self if p.x is not None]
        ys = [p.y for p in self if p.y is not None]

        if not xs or not ys:
            raise ValueError("No valid points to compute extremes")

        return max(xs), max(ys), min(xs), min(ys)

    def centroid(self) -> tuple[float, float]:
        if self.is_empty():
            raise ValueError("No points in stream")

        xs = [p.x for p in self if p.x is not None]
        ys = [p.y for p in self if p.y is not None]
        return (sum(xs) / len(xs)), (sum(ys) / len(ys))

    def dispersion(self) -> float:
        max_x, max_y, min_x, min_y = self.extremes()
        return (max_x - min_x) + (max_y - min_y)
