from trackers.GazePoint import GazePoint


class GazeStream:
    points: list[GazePoint]

    def __init__(self, data: list[GazePoint]) -> None:
        self.points = data

    def get_duration(self):
        return self.points[-1].timestamp - self.points[0].timestamp
