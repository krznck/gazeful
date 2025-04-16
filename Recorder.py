import queue
import threading
import time

from trackers.GazePoint import GazePoint

TIMEOUT = 0.1


class Recorder:
    path: str | None = None
    _queue: queue.Queue = queue.Queue()
    _thread: threading.Thread | None = None
    _stop_event: threading.Event = threading.Event()
    _start_timestamp: float = 0.0

    def _writer_thread(self):
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                data: GazePoint = self._queue.get(timeout=TIMEOUT)
                data = self._offset_gaze(data)
                print(data)
                self._queue.task_done()
            except queue.Empty:
                continue

    def write(self, data: GazePoint):
        if not self._stop_event.is_set() and self._thread is not None:
            self._queue.put(data)

    def start(self):
        if self._thread is None or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._writer_thread, daemon=True)
            self._thread.start()
            self._start_timestamp = time.monotonic()

    def stop(self):
        self._stop_event.set()

    def _offset_gaze(self, gp: GazePoint):
        return GazePoint(gp.x, gp.y, gp.timestamp - self._start_timestamp)
