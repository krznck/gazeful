"""Collection of gaze points with support for incremental calculation of statistics."""
from __future__ import annotations

from collections import deque
from typing import Deque, NamedTuple

from trackers.GazePoint import GazePoint


class NonMonotonicTimesstampError(Exception):
    """Raised when a GazePoint with a non-monotonic timestamp is added."""


class _ExtremesCache:
    """Internal cache for tracking the coordinate boundaries of a GazeStream.

    Attributes:
        max_x: Maximum normalized x coordinate.
        max_y: Maximum normalized y coordinate.
        min_x: Minimum normalized x coordinate.
        min_y: Minimum normalized y coordinate.
    """

    max_x: float
    max_y: float
    min_x: float
    min_y: float

    def __init__(self, initial: GazePoint | _ExtremesCache) -> None:
        """Initializes the cache from a point or another cache instance.

        Args:
            initial: Starting data for the extremes.
        """
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
        """Updates the extremes if the given point is outside current boundaries.

        Args:
            value: The gaze point to check.
        """
        if value.x is not None:
            self.max_x = max(self.max_x, value.x)
            self.min_x = min(self.min_x, value.x)
        if value.y is not None:
            self.max_y = max(self.max_y, value.y)
            self.min_y = min(self.min_y, value.y)

    def match(self, value: GazePoint) -> bool:
        """Checks if a point's coordinates match any of the cached extremes.

        Args:
            value: The point to check against.

        Returns:
            True if any coordinate is equal to a cached extreme.
        """
        return (
            value.x == self.max_x
            or value.x == self.min_x
            or value.y == self.max_y
            or value.y == self.min_y
        )

    def copy(self) -> _ExtremesCache:
        """Creates a copy of the cache."""
        return _ExtremesCache(self)


class _CentroidCache:
    """Internal cache for tracking the centroid of a GazeStream.

    Attributes:
        _sum_x: Running sum of all x coordinates.
        _sum_y: Running sum of all y coordinates.
        _len: Number of points included in the sums.
    """

    _sum_x: float
    _sum_y: float
    _len: int

    def __init__(self, initial: GazePoint | _CentroidCache) -> None:
        """Initializes the cache from a point or another cache instance.

        Args:
            initial: Starting data for the sums.

        Raises:
            RuntimeError: If the starting data contain empty points.
        """
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
        """Adds a point's coordinates to the running sums.

        Args:
            value: The gaze point to include.
        """
        if value.x is not None and value.y is not None:
            self._sum_x += value.x
            self._sum_y += value.y
            self._len += 1

    def discard(self, value: GazePoint):
        """Subtracts a point's coordinates from the running sums.

        Args:
            value: The gaze point to remove.
        """
        if value.x is not None and value.y is not None:
            self._sum_x -= value.x
            self._sum_y -= value.y
            self._len -= 1

    def copy(self) -> _CentroidCache:
        """Creates a copy of the cache."""
        return _CentroidCache(self)

    @property
    def centroid(self) -> tuple[float, float]:
        """Returns the current average (x, y) coordinates.

        Returns:
            A tuple of (average_x, average_y).
        """
        return (self._sum_x / self._len, self._sum_y / self._len)


class GazeStream:
    """A collection of GazePoints representing a continuous segment of gaze.

    This class maintains internal caches to provide performant access to extremes and
    centroid calculations as points are added or removed.

    Attributes:
        points: The sequence of GazePoints.
    """

    points: deque[GazePoint]
    _ex_cache: _ExtremesCache | None
    _cent_cache: _CentroidCache | None

    def __init__(
        self,
        data: list[GazePoint] | None | Deque = None,
    ) -> None:
        """Initializes the GazeStream.

        Args:
            data: Optional sequence of starting gaze points.
        """
        self.points = deque()
        self._ex_cache = None
        self._cent_cache = None
        if data is not None:
            self.points = deque(data)

    def __iter__(self):
        """Returns an iterator over the points."""
        return iter(self.points)

    def __len__(self) -> int:
        """Returns the number of points in the stream."""
        return len(self.points)

    def __getitem__(self, index: int) -> GazePoint:
        """Returns the GazePoint at the given index."""
        return self.points[index]

    def __str__(self) -> str:
        """Returns a string representation including the fixation duration."""
        builder = f"--- {self.duration()*1000}ms fixation ---"
        for point in self:
            builder += f"\n {point}"
        return builder

    def copy(self) -> GazeStream:
        """Creates a deep copy of the stream and its caches."""
        new = GazeStream(self.points.copy())
        # NOTE: Ignoring attribute privacy to not put this in constructor
        if self._ex_cache:
            new._ex_cache = self._ex_cache.copy()
        if self._cent_cache:
            new._cent_cache = self._cent_cache.copy()
        return new

    def append(self, point: GazePoint) -> None:
        """Appends a point to the end of the stream.

        Args:
            point: The gaze point to add.

        Raises:
            NonMonotonicTimesstampError: If the point's timestamp is before
                the current last point.
        """
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
        """Updates internal statistics with a new point."""
        self._offer_to_ex_cache(point)
        self._offer_to_cent_cache(point)

    def _offer_to_ex_cache(self, point: GazePoint) -> None:
        """Updates coordinate boundaries cache with a new point."""
        if point.are_eyes_closed():
            return
        if not self._ex_cache:
            self._ex_cache = _ExtremesCache(point)
        else:
            self._ex_cache.offer(point)

    def _offer_to_cent_cache(self, point: GazePoint) -> None:
        """Updates centroid calculation cache with a new point."""
        if point.are_eyes_closed():
            return
        if not self._cent_cache:
            self._cent_cache = _CentroidCache(point)
        else:
            self._cent_cache.offer(point)

    def pop(self) -> GazePoint:
        """Removes and returns the first point in the stream.

        Note:
            Invalidates the extremes cache if the removed point was an extreme.
        """
        p = self.points.popleft()
        if self._ex_cache and self._ex_cache.match(p):
            self._ex_cache = None
        if self._cent_cache:
            self._cent_cache.discard(p)
        return p

    def duration(self) -> float:
        """Calculates the time duration of the stream.

        Returns:
            The time in seconds between the first and last point.
        """
        if (len(self)) == 1:
            return self[0].timestamp
        elif (len(self)) == 0:
            return 0
        else:
            return self[-1].timestamp - self[0].timestamp

    def is_empty(self) -> bool:
        """Returns True if the stream has no points."""
        return len(self) <= 0

    def clear(self) -> None:
        """Clears all points and statistic caches."""
        self._ex_cache = None
        self._cent_cache = None
        self.points.clear()

    @property
    def extremes(self) -> Extremes:
        """Returns the coordinate boundaries of all open-eye points in the stream.

        Returns:
            The current coordinate bounds.

        Raises:
            RuntimeError: If there are no open-eye points to calculate extremes from.
        """
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
        """Returns the average (x, y) coordinates of the stream.

        Returns:
            A tuple of (average_x, average_y).

        Raises:
            RuntimeError: If there are no open-eye points to calculate centroid from.
        """
        c = self._cent_cache
        if not c:
            for point in self:
                self._offer_to_cent_cache(point)
        c = self._cent_cache

        if not c:
            raise RuntimeError("Attempted to access non-existant centroid")

        return c.centroid


class Extremes(NamedTuple):
    """Normalized coordinate bounds for a gaze segment.

    Attributes:
        max_x: Maximum x coordinate.
        max_y: Maximum y coordinate.
        min_x: Minimum x coordinate.
        min_y: Minimum y coordinate.
    """
    max_x: float
    max_y: float
    min_x: float
    min_y: float
