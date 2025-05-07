from processing.Definitions import Definitions
from processing.GazeStream import GazeStream


class ClosureAnalyzer:
    main_stream: GazeStream
    defs: Definitions
    closures: list[GazeStream] | None = None

    def __init__(self, data: GazeStream, defs: Definitions) -> None:
        self.main_stream = data
        self.defs = defs

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
        for point in self.main_stream.points:
            if point.are_eyes_closed():
                current.add(point)
            elif not current.is_empty():
                closures.append(current)
                current = GazeStream()

        if not current.is_empty():
            closures.append(current)

        return closures

    def __is_blink(self, segment: GazeStream) -> bool:
        return segment.get_duration() * 1000 <= self.defs.blink_threshhold_ms.value

    def __is_microsleep(self, segment: GazeStream) -> bool:
        return segment.get_duration() * 1000 >= self.defs.blink_threshhold_ms.value
