from PyQt6.QtCore import QObject
from editor.GazeModel import GazeModel
from typing import TYPE_CHECKING

# NOTE:
# This allows us to use `EditorPage` without a circular import problem.
# Note that the circular import problem is only there because `EditorPage` is dependent on this.
if TYPE_CHECKING:
    from editor.EditorPage import EditorPage


class EditorController(QObject):
    _view: "EditorPage"
    _model: GazeModel

    def __init__(self, view: "EditorPage", model: GazeModel) -> None:
        super().__init__()
        self._view = view
        self._model = model
        self._init_connections()

    def _init_connections(self) -> None:
        view, model = self._view, self._model
        model.recording_changed_sig.connect(self._recording_received)
        view.recording_selected.connect(lambda path: model.change_recording(path))

    # TODO: This works (receives recordings), but still doesn't actually do anything.
    # Should trigger the current VisualizationStrategy (currently nonexistant)
    # to render and hand over to the View our plot
    def _recording_received(self) -> None:
        rec = self._model.recording
        if rec is None:
            return

        print(rec.data)
