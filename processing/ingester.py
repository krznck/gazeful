import csv
from pathlib import Path

from processing.GazeRecording import GazeRecording
from processing.GazeStream import GazeStream
from recording.Recorder import EYE_CLOSED
from trackers.GazePoint import GazePoint
from trackers.GazePoint import list_fields


class InvalidFormatError(Exception):
    """Raised when the given file is not ingestible into gaze data."""

    pass


def ingest_csv(path: Path) -> GazeRecording:
    points = GazeStream()

    with path.open("r", newline="") as f:
        reader = csv.reader(f)

        valid_header = False
        screen_dimensions = None

        try:
            line = next(reader)
            if line[0][0] == "#":
                screen_dimensions = ingest_screen_dimension_comment(line[0])
                if next(reader) == list_fields():
                    valid_header = True
            elif line == list_fields():
                valid_header = True
        except StopIteration:  # can't go to next line -> obviously no header
            valid_header = False

        if not valid_header:
            raise InvalidFormatError(f"{path} does not start with a valid header.")

        for line_num, row in enumerate(reader, start=2):
            try:
                x = float(row[0]) if row[0] != EYE_CLOSED else None
                y = float(row[1]) if row[1] != EYE_CLOSED else None
                timestamp = float(row[2])
                points.append(GazePoint(x, y, timestamp))
            except (IndexError, ValueError):
                raise InvalidFormatError(
                    f"Invalid data encountered at row {line_num} in {path}"
                )

    return GazeRecording(data=points, screen_dimensions=screen_dimensions)


def ingest_screen_dimension_comment(line: str) -> tuple[int, int]:
    try:
        s = line.lstrip("#")
        w, h = s.split("x")
        return int(w), int(h)
    except ValueError:
        raise InvalidFormatError(f"{line} is not a correct screen dimensions comment")
