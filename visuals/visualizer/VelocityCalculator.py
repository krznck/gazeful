from collections import deque
from math import sqrt

from trackers.GazePoint import GazePoint

TIME_WINDOW_DEFAULT = 0.2  # 200ms
MAX_SAMPLES_DEFAULT = 60


class VelocityCalculator:
    velocity: float = 0.0
    window: float = TIME_WINDOW_DEFAULT
    history: deque = deque(maxlen=MAX_SAMPLES_DEFAULT)
    last_valid_point: GazePoint | None = None

    def update(self, gaze_point: GazePoint):
        self.history.append(gaze_point)

        if len(self.history) < 2:
            self.velocity = 0.0
            return

        self.__update_last_valid_point(gaze_point)

        if self.last_valid_point is not None:
            self.velocity = self.__calculate_velocity(self.last_valid_point, gaze_point)
            # print("Velocity: " + str(self.velocity))

    def __update_last_valid_point(self, current_point: GazePoint):
        if self.last_valid_point is None:
            self.last_valid_point = current_point
            return

        if current_point.timestamp - self.last_valid_point.timestamp >= self.window:
            self.last_valid_point = current_point

    def __calculate_velocity(self, old: GazePoint, new: GazePoint) -> float:
        if new.x is None or new.y is None or old.x is None or old.y is None:
            return 0.0

        dx = new.x - old.x
        dy = new.y - old.y
        dt = new.timestamp - old.timestamp

        if dt <= 0:
            return 0.0

        distance = sqrt(dx * dx + dy * dy)
        return distance / dt
