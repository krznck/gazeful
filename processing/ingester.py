import csv
from pathlib import Path

from processing.GazeStream import GazeStream
from recording.Recorder import EYE_CLOSED
from trackers.GazePoint import GazePoint
from trackers.GazePoint import list_fields


class InvalidFormatError(Exception):
    """Raised when the given file is not ingestible into gaze data."""

    pass


def ingest_csv(path: Path) -> GazeStream:
    points = GazeStream()

    with path.open("r", newline="") as f:
        reader = csv.reader(f)

        valid_header = False

        try:
            valid_header = next(reader) == list_fields()
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

    return points
