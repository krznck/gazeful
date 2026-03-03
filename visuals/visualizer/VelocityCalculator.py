"""Tool for calculating movement velocity of gaze data."""
from collections import deque
from math import sqrt

from trackers.GazePoint import GazePoint

TIME_WINDOW_DEFAULT = 0.2  # 200ms
MAX_SAMPLES_DEFAULT = 60


class VelocityCalculator:
    """Calculates instantaneous velocity based on a sliding window of gaze points.

    Attributes:
        velocity: Calculated velocity in units/second.
        window: Time window in seconds for the calculation.
        history: Deque of historical gaze points.
        last_valid_point: Reference point for the current velocity calculation.
    """

    velocity: float = 0.0
    window: float = TIME_WINDOW_DEFAULT
    history: deque = deque(maxlen=MAX_SAMPLES_DEFAULT)
    last_valid_point: GazePoint | None = None

    def update(self, gaze_point: GazePoint):
        """Adds a new point and updates the velocity calculation.

        Args:
            gaze_point: Current gaze point.
        """
        self.history.append(gaze_point)

        if len(self.history) < 2:
            self.velocity = 0.0
            return

        self.__update_last_valid_point(gaze_point)

        if self.last_valid_point is not None:
            self.velocity = self.__calculate_velocity(self.last_valid_point, gaze_point)
            # print("Velocity: " + str(self.velocity))

    def __update_last_valid_point(self, current_point: GazePoint):
        """Updates the internal reference point if enough time has passed.

        Args:
            current_point: The latest gaze point.
        """
        if self.last_valid_point is None:
            self.last_valid_point = current_point
            return

        if current_point.timestamp - self.last_valid_point.timestamp >= self.window:
            self.last_valid_point = current_point

    def __calculate_velocity(self, old: GazePoint, new: GazePoint) -> float:
        """Calculates distance/time velocity between two points.

        Args:
            old: The reference (earlier) gaze point.
            new: The latest (later) gaze point.

        Returns:
            Calculated velocity.
        """
        if new.x is None or new.y is None or old.x is None or old.y is None:
            return 0.0

        dx = new.x - old.x
        dy = new.y - old.y
        dt = new.timestamp - old.timestamp

        if dt <= 0:
            return 0.0

        distance = sqrt(dx * dx + dy * dy)
        return distance / dt
