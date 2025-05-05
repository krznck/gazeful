from trackers.GazePoint import GazePoint


class GazeStream:
    points: list[GazePoint]

    def __init__(self, data: list[GazePoint] | None = None) -> None:
        self.points = []
        if data is not None:
            self.points = data

    def add(self, point: GazePoint) -> None:
        self.points.append(point)

    def get_duration(self) -> float:
        return (
            0
            if self.is_empty()
            else self.points[-1].timestamp - self.points[0].timestamp
        )

    def is_empty(self) -> bool:
        return len(self.points) <= 0
