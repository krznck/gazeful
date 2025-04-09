from collections import deque

from trackers.GazePoint import GazePoint


class VelocityCalculator:
    history: deque

    def __init__(self, max_samples: int = 5) -> None:
        self.history = deque(maxlen=max_samples)

    def update(self, gaze_point: GazePoint):
        self.history.append((gaze_point))

        # print("History: ", list(self.history))
