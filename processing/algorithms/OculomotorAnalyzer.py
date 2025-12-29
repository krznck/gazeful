import statistics

from processing.GazeRecording import GazeRecording
from processing.GazeStream import GazeStream
from processing.algorithms.BaseAnalyzer import BaseAnalyzer


class OculomotorAnalyzer(BaseAnalyzer):
    _fixations: list[GazeStream] | None
    _average: float | None
    _median: float | None

    _fixation_min_duration_ms: float
    _fixation_max_dispersion_px: float

    def __init__(
        self,
        data: GazeRecording,
        fixation_min_duration_ms: float,
        fixation_max_dispersion_px: float,
    ) -> None:
        super().__init__(data)
        self._fixations = None
        self._average = None
        self._median = None
        self._fixation_min_duration_ms = fixation_min_duration_ms
        self._fixation_max_dispersion_px = fixation_max_dispersion_px

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
        if self._fixations is None:
            self._calculate_statistics()

        assert self._fixations is not None
        return max(point.duration() for point in self._fixations)

    def _calculate_statistics(self) -> None:
        if self._fixations is None:
            self._fixations = self.extract_fixations()

        duration_ms = [fix.duration() * 1000 for fix in self._fixations]
        if len(self._fixations) < 1:
            self._average = 0
            self._median = 0
            return
        self._average = statistics.mean(duration_ms)
        self._median = statistics.median(duration_ms)

    def extract_fixations(self) -> list[GazeStream]:
        fixations: list[GazeStream] = []
        window = GazeStream()

        for candidate in self.recording.data:
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
                    future.pop()
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
        return norm >= self._fixation_min_duration_ms

    def _is_within_dispersion(self, segment: GazeStream):
        if len(segment) < 2:
            return True

        sw, sh = self.recording.screen
        extremes = segment.extremes
        dx_norm = extremes.max_x - extremes.min_x
        dy_norm = extremes.max_y - extremes.min_y
        dx_px = dx_norm * sw
        dy_px = dy_norm * sh

        return (dx_px + dy_px) <= self._fixation_max_dispersion_px
