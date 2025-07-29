from __future__ import annotations

from collections import deque
from typing import Deque
from typing import NamedTuple

from trackers.GazePoint import GazePoint


class NonMonotonicTimesstampError(Exception):
    """Raised when a GazePoint with a non-monotonic timestamp is added."""


class _ExtremesCache:
    max_x: float
    max_y: float
    min_x: float
    min_y: float

    def __init__(self, initial: GazePoint | _ExtremesCache) -> None:
        match initial:
            case GazePoint():
                if initial.x is None or initial.y is None:
                    raise RuntimeError("Attempted to cache empty points")
                self.max_x = initial.x
                self.max_y = initial.y
                self.min_x = initial.x
                self.min_y = initial.y
            case _ExtremesCache():
                self.max_x = initial.max_x
                self.max_y = initial.max_y
                self.min_x = initial.min_x
                self.min_y = initial.min_y

    def offer(self, value: GazePoint):
        if value.x is not None:
            self.max_x = max(self.max_x, value.x)
            self.min_x = min(self.min_x, value.x)
        if value.y is not None:
            self.max_y = max(self.max_y, value.y)
            self.min_y = min(self.min_y, value.y)

    def match(self, value: GazePoint) -> bool:
        return (
            value.x == self.max_x
            or value.x == self.min_x
            or value.y == self.max_y
            or value.y == self.min_y
        )

    def copy(self) -> _ExtremesCache:
        return _ExtremesCache(self)


class _CentroidCache:
    _sum_x: float
    _sum_y: float
    _len: int

    def __init__(self, initial: GazePoint | _CentroidCache) -> None:
        match initial:
            case GazePoint():
                if initial.x is None or initial.y is None:
                    raise RuntimeError("Attempted to cache empty points")
                self._sum_x = initial.x
                self._sum_y = initial.y
                self._len = 1
            case _CentroidCache():
                self._sum_x = initial._sum_x
                self._sum_y = initial._sum_y
                self._len = initial._len

    def offer(self, value: GazePoint):
        if value.x is not None and value.y is not None:
            self._sum_x += value.x
            self._sum_y += value.y
            self._len += 1

    def discard(self, value: GazePoint):
        if value.x is not None and value.y is not None:
            self._sum_x -= value.x
            self._sum_y -= value.y
            self._len -= 1

    def copy(self) -> _CentroidCache:
        return _CentroidCache(self)

    @property
    def centroid(self) -> tuple[float, float]:
        return (self._sum_x / self._len, self._sum_y / self._len)


class GazeStream:
    points: deque[GazePoint]
    _ex_cache: _ExtremesCache | None
    _cent_cache: _CentroidCache | None

    def __init__(
        self,
        data: list[GazePoint] | None | Deque = None,
    ) -> None:
        self.points = deque()
        self._ex_cache = None
        self._cent_cache = None
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

    def copy(self) -> GazeStream:
        new = GazeStream(self.points.copy())
        # NOTE: Ignoring attribute privacy to not put this in constructor
        if self._ex_cache:
            new._ex_cache = self._ex_cache.copy()
        if self._cent_cache:
            new._cent_cache = self._cent_cache.copy()
        return new

    def append(self, point: GazePoint) -> None:
        if len(self) == 0:
            self.points.append(point)
            self._offer_to_caches(point)
            return

        last = self[-1].timestamp
        if point.timestamp < last:
            raise NonMonotonicTimesstampError(
                f"Tried to add point with timestamp {point.timestamp} after {last}"
            )

        self.points.append(point)
        self._offer_to_caches(point)

    def _offer_to_caches(self, point: GazePoint) -> None:
        self._offer_to_ex_cache(point)
        self._offer_to_cent_cache(point)

    def _offer_to_ex_cache(self, point: GazePoint) -> None:
        if point.are_eyes_closed():
            return
        if not self._ex_cache:
            self._ex_cache = _ExtremesCache(point)
        else:
            self._ex_cache.offer(point)

    def _offer_to_cent_cache(self, point: GazePoint) -> None:
        if point.are_eyes_closed():
            return
        if not self._cent_cache:
            self._cent_cache = _CentroidCache(point)
        else:
            self._cent_cache.offer(point)

    def pop(self) -> GazePoint:
        p = self.points.popleft()
        if self._ex_cache and self._ex_cache.match(p):
            self._ex_cache = None
        if self._cent_cache:
            self._cent_cache.discard(p)
        return p

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
        self._ex_cache = None
        self._cent_cache = None
        self.points.clear()

    @property
    def extremes(self) -> Extremes:
        c = self._ex_cache
        if not c:
            for point in self:
                if point.are_eyes_open():
                    self._offer_to_ex_cache(point)
        c = self._ex_cache

        if not c:
            raise RuntimeError("Attempted to gather empty extremes")

        return Extremes(max_x=c.max_x, max_y=c.max_y, min_x=c.min_x, min_y=c.min_y)

    @property
    def centroid(self) -> tuple[float, float]:
        c = self._cent_cache
        if not c:
            for point in self:
                self._offer_to_cent_cache(point)
        c = self._cent_cache

        if not c:
            raise RuntimeError("Attempted to access non-existant centroid")

        return c.centroid


class Extremes(NamedTuple):
    max_x: float
    max_y: float
    min_x: float
    min_y: float
