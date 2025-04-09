from collections import deque
from math import sqrt

from trackers.GazePoint import GazePoint


class VelocityCalculator:
    __history: deque
    velocity: float = 0.0

    def __init__(self, max_samples: int = 20) -> None:
        self.__history = deque(maxlen=max_samples)

    def update(self, gaze_point: GazePoint):
        self.__history.append((gaze_point))
        self.__calculate_velocity()
        # print("Velocity: " + str(self.velocity))

    def __calculate_velocity(self) -> None:
        if len(self.__history) < 2:
            self.velocity = 0.0
            return

        newest: GazePoint = self.__history[-1]
        if newest.are_eyes_closed():  # eyes are newly closed, so velocity stops dead
            self.velocity = 0.0
            return

        oldest = self.__find_oldest_open()

        if oldest is None:  # no point in which eyes were open
            self.velocity = 0.0
            return

        assert newest.x is not None and newest.y is not None
        assert oldest.x is not None and oldest.y is not None

        dx = newest.x - oldest.x
        dy = newest.y - oldest.y
        dt = newest.timestamp - oldest.timestamp

        # ISSUE: Maybe change this to an exception?
        if dt == 0:
            self.velocity = 0.0
            return

        distance = sqrt(dx * dx + dy * dy)
        self.velocity = distance / dt

    def __find_oldest_open(self) -> GazePoint | None:
        for point in self.__history:
            point: GazePoint
            if point.are_eyes_open():
                return point

        return None
