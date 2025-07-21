import csv
import queue
import threading
import time
from pathlib import Path

from PyQt6.QtGui import QScreen

from processing.GazeRecording import GazeRecording
from processing.GazeStream import GazeStream
from recording.screenshots import shoot_screen
from trackers.GazePoint import GazePoint
from trackers.GazePoint import list_fields

TIMEOUT = 0.1
EYE_CLOSED = "NA"
EXTENSION = ".csv"


class Recorder:
    path: Path | None
    _queue: queue.Queue
    _thread: threading.Thread | None
    _stop_event: threading.Event
    _start_timestamp: float
    _screenshot_path: Path | None

    def __init__(self, screen: tuple[int, int]) -> None:
        self.path = None
        self._queue = queue.Queue()
        self._thread = None
        self._stop_event = threading.Event()
        self._screen = screen
        self._recording = GazeStream()
        self._screenshot_path = None

    def set_screen(self, screen: tuple[int, int]) -> None:
        self._screen = screen

    def _writer_thread(self) -> None:
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
        if not self._stop_event.is_set() and self._thread is not None:
            self._queue.put(data)

    def start(self, path: Path, screenshot_screen: QScreen | None = None) -> None:
        self._recording.clear()
        if screenshot_screen:
            ss_path = coerce_screenshot_path(path)
            shoot_screen(screenshot_screen, ss_path)
            self._screenshot_path = ss_path
        self.path = coerce_csv(path)
        if self._thread is None or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._writer_thread, daemon=True)
            self._thread.start()
            self._start_timestamp = time.monotonic()

    def stop(self) -> GazeRecording:
        self._stop_event.set()
        return GazeRecording(
            data=self._recording,
            screen_dimensions=self._screen,
            screenshot=self._screenshot_path,
        )

    def _offset_gaze(self, gp: GazePoint) -> GazePoint:
        return GazePoint(gp.x, gp.y, max((gp.timestamp - self._start_timestamp), 0))


def coerce_csv(path: Path) -> Path:
    if path.suffix != EXTENSION:
        return path.with_suffix(EXTENSION)
    return path


def coerce_screenshot_path(path: Path) -> Path:
    new = path.with_name(f"{path.stem}-screenshot.png")
    return new


def file_already_saved(path: Path) -> bool:
    return coerce_csv(path).exists()
