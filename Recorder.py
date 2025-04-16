import queue
import threading

from trackers.GazePoint import GazePoint

TIMEOUT = 0.1


class Recorder:
    path: str | None = None
    _queue: queue.Queue = queue.Queue()
    _thread: threading.Thread | None = None
    _stop_event: threading.Event = threading.Event()

    def _writer_thread(self):
        while not self._stop_event.is_set() or not self._queue.empty():
            try:
                data = self._queue.get(timeout=TIMEOUT)
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

    def stop(self):
        self._stop_event.set()
