from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal
from AppContext import AppContext
from processing.GazeRecording import GazeRecording
from processing.algorithms.OculomotorAnalyzer import OculomotorAnalyzer
from processing.ingester import ingest_csv


# NOTE: Needs to be QObject to have access to signals.
class GazeModel(QObject):
    recording_changed_sig = pyqtSignal()

    recording: GazeRecording | None
    _context: AppContext
    _analyzer: OculomotorAnalyzer | None
    _background_cache: Path | None

    def __init__(self, context: AppContext) -> None:
        super().__init__()
        self._context = context
        self.recording = context.main_data
        self._analyzer = None
        self._background_cache = None

        context.main_data_changed.connect(self._recording_changed)

    def _recording_changed(self) -> None:
        self.recording = self._context.main_data
        self.recording_changed_sig.emit()

    def change_recording(self, path: str) -> None:
        recording = ingest_csv(Path(path))
        if bg := self._background_cache:
            recording.screenshot = bg
        self._context.main_data = recording

    def change_background(self, path: str) -> None:
        r = self.recording
        if r is None:
            self._background_cache = Path(path)
            return

        r.screenshot = Path(path)
        self.recording_changed_sig.emit()
