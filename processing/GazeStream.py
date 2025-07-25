from __future__ import annotations

from collections import deque
from functools import cached_property
from typing import Deque

from trackers.GazePoint import GazePoint


class NonMonotonicTimesstampError(Exception):
    """Raised when a GazePoint with a non-monotonic timestamp is added."""


class GazeStream:
    points: deque[GazePoint]
    _cached_properties = ["extremes", "centroid"]

    def __init__(
        self,
        data: list[GazePoint] | None | Deque = None,
    ) -> None:
        self.points = deque()
        if data is not None:
            self.points = deque(data)

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

    def _invalidate_caches(self) -> None:
        for property in self._cached_properties:
            if property in self.__dict__:
                del self.__dict__[property]

    def copy(self) -> GazeStream:
        new = GazeStream(self.points.copy())
        for property in self._cached_properties:
            if property in self.__dict__:
                new.__dict__[property] = self.__dict__[property]
        return new

    def append(self, point: GazePoint) -> None:
        if len(self) == 0:
            self._invalidate_caches()
            self.points.append(point)
            return

        last = self[-1].timestamp
        if point.timestamp < last:
            raise NonMonotonicTimesstampError(
                f"Tried to add point with timestamp {point.timestamp} after {last}"
            )

        self._invalidate_caches()
        self.points.append(point)

    def pop(self) -> GazePoint:
        self._invalidate_caches()
        return self.points.popleft()

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
        self._invalidate_caches()
        self.points.clear()

    @cached_property
    def extremes(self) -> tuple[float, float, float, float]:
        xs = [p.x for p in self if p.x is not None]
        ys = [p.y for p in self if p.y is not None]

        if not xs or not ys:
            raise ValueError("No valid points to compute extremes")

        return max(xs), max(ys), min(xs), min(ys)

    @cached_property
    def centroid(self) -> tuple[float, float]:
        if self.is_empty():
            raise ValueError("No points in stream")

        xs = [p.x for p in self if p.x is not None]
        ys = [p.y for p in self if p.y is not None]
        return (sum(xs) / len(xs)), (sum(ys) / len(ys))

    def dispersion(self) -> float:
        max_x, max_y, min_x, min_y = self.extremes
        return (max_x - min_x) + (max_y - min_y)
