from trackers.GazePoint import GazePoint


class GazeStream:
    points: list[GazePoint]

    def __init__(self, data: list[GazePoint] | None = None) -> None:
        self.points = []
        if data is not None:
            self.points = data

    def add(self, point: GazePoint) -> None:
        self.points.append(point)

    def pop_first(self) -> GazePoint:
        return self.points.pop(0)

    def get_duration(self) -> float:
        if len(self.points) == 1:
            return self.points[0].timestamp
        elif len(self.points) == 0:
            return 0
        else:
            return self.points[-1].timestamp - self.points[0].timestamp

    def is_empty(self) -> bool:
        return len(self.points) <= 0
