import csv
import queue
import threading
import time
from pathlib import Path

from trackers.GazePoint import GazePoint
from trackers.GazePoint import list_fields

TIMEOUT = 0.1
EYE_CLOSED = "NA"
EXTENSION = ".csv"


class Recorder:
    path: Path | None = None
    _queue: queue.Queue = queue.Queue()
    _thread: threading.Thread | None = None
    _stop_event: threading.Event = threading.Event()
    _start_timestamp: float = 0.0

    def _writer_thread(self) -> None:
        if self.path is None:
            return

        with open(self.path, "a", newline="") as f:
            writer = csv.writer(f)

            if f.tell() == 0:
                writer.writerow(list_fields())

            while not self._stop_event.is_set() or not self._queue.empty():
                try:
                    data: GazePoint = self._queue.get(timeout=TIMEOUT)
                    data = self._offset_gaze(data)
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

    def start(self, path: Path) -> None:
        self.path = coerce_csv(path)
        if self._thread is None or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._writer_thread, daemon=True)
            self._thread.start()
            self._start_timestamp = time.monotonic()

    def stop(self) -> None:
        self._stop_event.set()

    def _offset_gaze(self, gp: GazePoint) -> GazePoint:
        return GazePoint(gp.x, gp.y, gp.timestamp - self._start_timestamp)


def coerce_csv(path: Path) -> Path:
    if path.suffix != EXTENSION:
        return path.with_suffix(EXTENSION)
    return path
