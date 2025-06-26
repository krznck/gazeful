import statistics

from processing.algorithms.BaseAnalyzer import BaseAnalyzer
from processing.Definitions import Definitions
from processing.GazeStream import GazeStream


class OculomotorAnalyzer(BaseAnalyzer):
    def __init__(self, data: GazeStream, defs: Definitions) -> None:
        super().__init__(data, defs)
        self.fixations: list[GazeStream] | None = None
        self._average: float | None = None
        self._median: float | None = None

    def median_fixation_duration(self) -> float:
        if self._median is None:
            self._calculate_statistics()

        assert self._median is not None
        return self._median

    def average_fixation_duration(self) -> float:
        if self._average is None:
            self._calculate_statistics()

        assert self._average is not None
        return self._average

    def longest_fixation_duration(self) -> float:
        if self.fixations is None:
            self._calculate_statistics()

        assert self.fixations is not None
        return max(point.duration() for point in self.fixations)

    def _calculate_statistics(self) -> None:
        if self.fixations is None:
            self.fixations = self.extract_fixations()

        duration_ms = [fix.duration() * 1000 for fix in self.fixations]
        self._average = statistics.mean(duration_ms)
        self._median = statistics.median(duration_ms)

    def extract_fixations(self) -> list[GazeStream]:
        fixations: list[GazeStream] = []
        window = GazeStream()

        for candidate in self.main_stream:
            # we discard right away on eyes being closed
            if candidate.are_eyes_closed():
                self._save_if_valid(fixations, window)
                continue

            future = window.copy()
            future.append(candidate)

            if self._is_within_dispersion(future):
                # the fixation is growing -> accept
                window = future
            elif self._save_if_valid(fixations, window):
                # the candidate breaks the fixation, but it was valid before
                window.append(candidate)
            else:
                # the candidate breaks the bounds, but it was too short
                # so we slide until it is within bounds
                while not self._is_within_dispersion(future):
                    if len(future) <= 1:
                        break
                    future.pop(0)
                window = future

        self._save_if_valid(fixations, window)
        return fixations

    def _save_if_valid(self, target: list[GazeStream], window: GazeStream) -> bool:
        if self._valid_fixation(window):
            target.append(window.copy())
            window.clear()
            return True
        return False

    def _valid_fixation(self, segment: GazeStream) -> bool:
        return (
            not segment.is_empty()
            and self._is_within_duration(segment)
            and self._is_within_dispersion(segment)
        )

    def _is_within_duration(self, segment: GazeStream):
        if len(segment) < 2:
            return False

        norm = segment.duration() * 1000
        return norm >= self.defs.fixation_minimum_duration_ms.value

    def _is_within_dispersion(self, segment: GazeStream):
        if len(segment) < 2:
            return True

        allowed = self.defs.fixation_maximum_dispersion_screen_area_percent.value
        return segment.dispersion() <= allowed
