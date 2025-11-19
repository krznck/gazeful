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

    def __init__(self, context: AppContext) -> None:
        super().__init__()
        self._context = context
        self.recording = context.main_data
        self._analyzer = None

        context.main_data_changed.connect(self._recording_changed)

    def _recording_changed(self) -> None:
        self.recording = self._context.main_data
        self.recording_changed_sig.emit()

    def change_recording(self, path: str) -> None:
        self._context.main_data = ingest_csv(Path(path))
