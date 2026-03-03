"""Core recording logic for capturing gaze data to persistent storage."""
import csv
import queue
import threading
import time
from pathlib import Path

from processing.GazeRecording import GazeRecording
from processing.GazeStream import GazeStream
from PyQt6.QtGui import QScreen
from trackers.GazePoint import GazePoint, list_fields

from recording.screenshots import shoot_screen

TIMEOUT = 0.1
EYE_CLOSED = "NA"
EXTENSION = ".csv"


class Recorder:
    """Manages the recording process by writing gaze data to a CSV file in the background.

    Attributes:
        path: Path to the CSV file being written.
        _queue: Internal queue for thread-safe data transfer.
        _thread: Background thread that handles file IO.
        _stop_event: Event used to signal the background thread to stop.
        _start_timestamp: Reference time when recording started.
        _screenshot_path: Path where a screenshot of the recording was saved.
    """

    path: Path | None
    _queue: queue.Queue
    _thread: threading.Thread | None
    _stop_event: threading.Event
    _start_timestamp: float
    _screenshot_path: Path | None

    def __init__(self, screen: tuple[int, int]) -> None:
        """Initializes the recorder.

        Args:
            screen: Dimensions (width, height) of the screen being recorded.
        """
        self.path = None
        self._queue = queue.Queue()
        self._thread = None
        self._stop_event = threading.Event()
        self._screen = screen
        self._recording = GazeStream()
        self._screenshot_path = None

    def set_screen(self, screen: tuple[int, int]) -> None:
        """Updates the screen dimensions used for coordinate normalization.

        Args:
            screen: New screen dimensions (width, height).
        """
        self._screen = screen

    def _writer_thread(self) -> None:
        """Internal background loop that writes gaze data to the CSV file."""
        if self.path is None:
            return

        self.path.parent.mkdir(parents=True, exist_ok=True)  # need to create parents
        with self.path.open("w", newline="") as f:
            writer = csv.writer(f)

            if f.tell() == 0:
                writer.writerow([f"#{self._screen[0]}x{self._screen[1]}"])
                writer.writerow(list_fields())

            while not self._stop_event.is_set() or not self._queue.empty():
                try:
                    data: GazePoint = self._queue.get(timeout=TIMEOUT)
                    data = self._offset_gaze(data)
                    self._recording.append(data)
                    row = [
                        EYE_CLOSED if data.x is None else data.x,
                        EYE_CLOSED if data.y is None else data.y,
                        data.timestamp,
                    ]
                    writer.writerow(row)
                    f.flush()
                    self._queue.task_done()
                except queue.Empty:
                    continue

    def write(self, data: GazePoint) -> None:
        """Queues a new gaze point to be written to file.

        Args:
            data: The gaze point to record.
        """
        if not self._stop_event.is_set() and self._thread is not None:
            self._queue.put(data)

    def start(self, path: Path, screenshot_screen: QScreen | None = None) -> None:
        """Starts the background recording thread.

        Args:
            path: Destination path for the CSV file.
            screenshot_screen: Optional screen object to capture a screenshot from.
        """
        self._recording.clear()
        self.path = coerce_csv(path)
        if screenshot_screen:
            ss_path = coerce_screenshot_path(self.path)
            shoot_screen(screenshot_screen, ss_path)
            self._screenshot_path = ss_path
        if self._thread is None or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._writer_thread, daemon=True)
            self._thread.start()
            self._start_timestamp = time.monotonic()

    def stop(self) -> GazeRecording:
        """Signals the recording thread to stop and returns the captured data.

        Returns:
            A GazeRecording object containing the recorded data and metadata.
        """
        self._stop_event.set()
        return GazeRecording(
            data=self._recording,
            screen_dimensions=self._screen,
            screenshot=self._screenshot_path,
        )

    def _offset_gaze(self, gp: GazePoint) -> GazePoint:
        """Adjusts a gaze point's timestamp relative to the recording start time.

        Args:
            gp: The original gaze point.

        Returns:
            A new gaze point with the adjusted timestamp.
        """
        return GazePoint(gp.x, gp.y, max((gp.timestamp - self._start_timestamp), 0))


def coerce_csv(path: Path) -> Path:
    """Ensures that a path has a .csv extension.

    Args:
        path: The original path.

    Returns:
        The path with a .csv suffix.
    """
    if path.suffix != EXTENSION:
        return path.with_suffix(EXTENSION)
    return path


def coerce_screenshot_path(path: Path) -> Path:
    """Generates a screenshot filename derived from a CSV file path.

    Args:
        path: The path to the CSV recording.

    Returns:
        A path for the screenshot with a '-screenshot.png' suffix.
    """
    new = path.with_name(f"{path.stem}-screenshot.png")
    return new


def file_already_saved(path: Path) -> bool:
    """Checks if a recording file already exists at the given path.

    Args:
        path: The path to check.

    Returns:
        True if the file exists.
    """
    return coerce_csv(path).exists()
