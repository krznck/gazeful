from processing.Definitions import Definitions
from processing.GazeStream import GazeStream


def extract_blinks(segment: GazeStream, defs: Definitions) -> list[GazeStream]:
    blinks = []
    current = GazeStream()
    for point in segment.points:
        if point.are_eyes_closed():
            current.add(point)
        else:
            if is_blink(current, defs):
                blinks.append(current)
            current = GazeStream()

    if not current.is_empty():  # need to account for segment ending on closed eyes
        if is_blink(current, defs):
            blinks.append(current)

    return blinks


# ISSUE: This is obviously quite lazy and inefficient. Consider a better approach.


def extract_microsleeps(segment: GazeStream, defs: Definitions) -> list[GazeStream]:
    blinks = []
    current = GazeStream()
    for point in segment.points:
        if point.are_eyes_closed():
            current.add(point)
        else:
            if is_microsleep(current, defs):
                blinks.append(current)
            current = GazeStream()

    if not current.is_empty():  # need to account for segment ending on closed eyes
        if is_microsleep(current, defs):
            blinks.append(current)

    return blinks


def is_blink(segment: GazeStream, defs: Definitions) -> bool:
    if not __all_closed(segment):
        return False
    return segment.get_duration() * 1000 <= defs.blink_threshhold_ms


def is_microsleep(segment: GazeStream, defs: Definitions) -> bool:
    if not __all_closed(segment):
        return False
    return segment.get_duration() * 1000 >= defs.blink_threshhold_ms


def __all_closed(segment: GazeStream) -> bool:
    return (not segment.is_empty()) and all(
        point.are_eyes_closed() for point in segment.points
    )
