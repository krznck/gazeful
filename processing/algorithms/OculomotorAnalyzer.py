import statistics
from dataclasses import dataclass
from dataclasses import fields
from os import stat

from processing.algorithms.BaseAnalyzer import BaseAnalyzer
from processing.GazeStream import GazeStream
from trackers.GazePoint import GazePoint


@dataclass
class Extremes:
    max_x: GazePoint
    max_y: GazePoint
    min_x: GazePoint
    min_y: GazePoint

    def update(self, point: GazePoint):
        self.max_x = point if point.compare_x(self.max_x) >= 0 else self.max_x
        self.max_y = point if point.compare_y(self.max_y) >= 0 else self.max_y
        self.min_x = point if point.compare_x(self.min_x) <= 0 else self.min_x
        self.min_y = point if point.compare_y(self.min_y) <= 0 else self.min_y

    def dispersion(self) -> float:
        assert self.max_x.x is not None and self.min_x.x is not None
        assert self.max_y.y is not None and self.min_y.y is not None
        # should not even be called if an extreme is closed,
        # since we don't want closures!
        return (self.max_x.x - self.min_x.x) + (self.max_y.y - self.min_y.y)

    def check_removal(self, removed: GazePoint, window: GazeStream):
        invalid = False
        for field in fields(self):
            extreme = getattr(self, field.name)
            if removed == extreme:
                invalid = True

        # NOTE: If the removed point was an extreme,
        # we have to find a different extreme.
        # I do think this sucks a little, but unsure of a smarter way.
        if invalid:
            for field in fields(self):
                extreme = setattr(self, field.name, window.points[0])
            for point in window.points[1:]:
                self.update(point)


class OculomotorAnalyzer(BaseAnalyzer):
    fixations: list[GazeStream] | None = None
    _average: float | None = None
    _median: float | None = None

    def median_fixation_duration(self) -> float:
        if self._median is None:
            self.__calculate_statistics()

        assert self._median is not None
        return self._median

    def average_fixation_duration(self) -> float:
        if self._average is None:
            self.__calculate_statistics()

        assert self._average is not None
        return self._average

    def extract_fixations(self) -> list[GazeStream]:
        fixations = []

        window = GazeStream()
        extremes = None
        for point in self.main_stream.points:
            if point.are_eyes_closed():
                if not window.is_empty() and self.__is_within_duration(window):
                    fixations.append(window)
                window = GazeStream()
                extremes = None
                continue

            window.add(point)

            if extremes is None:
                extremes = Extremes(point, point, point, point)

            extremes.update(point)

            if not self.__is_within_dispersion(extremes.dispersion()):
                if self.__is_within_duration(window):
                    fixations.append(window)
                    window = GazeStream()
                    extremes = None
                    continue
                removed = window.pop_first()
                extremes.check_removal(removed, window)

        if not window.is_empty() and self.__is_within_duration(window):
            fixations.append(window)

        return fixations

    def __is_within_duration(self, segment: GazeStream) -> bool:
        norm_duration = segment.get_duration() * 1000
        return norm_duration >= self.defs.fixation_minimum_duration_ms.value

    def __is_within_dispersion(self, current_disp: float) -> bool:
        allowed = self.defs.fixation_maximum_dispersion_screen_area_percent.value
        return current_disp <= allowed

    def __calculate_statistics(self) -> None:
        if self.fixations is None:
            self.fixations = self.extract_fixations()

        duration_ms = [fix.get_duration() * 1000 for fix in self.fixations]
        self._average = statistics.mean(duration_ms)
        self._median = statistics.median(duration_ms)
