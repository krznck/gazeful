from processing.algorithms.BaseAnalyzer import BaseAnalyzer
from processing.GazeStream import GazeStream


class ClosureAnalyzer(BaseAnalyzer):
    closures: list[GazeStream] | None = None

    def extract_blinks(self) -> list[GazeStream]:
        if self.closures is None:
            self.closures = self.__extract_closures()

        blinks = []
        for segment in self.closures:
            if self.__is_blink(segment):
                blinks.append(segment)

        return blinks

    def extract_microsleeps(self) -> list[GazeStream]:
        if self.closures is None:
            self.closures = self.__extract_closures()

        blinks = []
        for segment in self.closures:
            if self.__is_microsleep(segment):
                blinks.append(segment)

        return blinks

    def __extract_closures(self) -> list[GazeStream]:
        closures = []
        current = GazeStream()
        for point in self.main_stream:
            if point.are_eyes_closed():
                current.append(point)
            elif not current.is_empty():
                closures.append(current)
                current = GazeStream()

        if not current.is_empty():
            closures.append(current)

        return closures

    def __is_blink(self, segment: GazeStream) -> bool:
        return segment.duration() * 1000 <= self.defs.blink_threshhold_ms.value

    def __is_microsleep(self, segment: GazeStream) -> bool:
        return segment.duration() * 1000 >= self.defs.blink_threshhold_ms.value
