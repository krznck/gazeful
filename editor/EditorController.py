from PyQt6.QtCore import QObject
from editor.GazeModel import GazeModel
from typing import TYPE_CHECKING

from editor.VisualizationStrategy import VisualizationStrategy

# NOTE:
# This allows us to use `EditorPage` without a circular import problem.
# Note that the circular import problem is only there because `EditorPage` is dependent on this.
if TYPE_CHECKING:
    from editor.EditorPage import EditorPage


class EditorController(QObject):
    _view: "EditorPage"
    _model: GazeModel
    _vis_strat: VisualizationStrategy

    def __init__(
        self,
        view: "EditorPage",
        model: GazeModel,
        visualization_strategy: VisualizationStrategy,
    ) -> None:
        super().__init__()
        self._view = view
        self._model = model
        self._vis_strat = visualization_strategy
        self._init_connections()

    def _init_connections(self) -> None:
        view, model = self._view, self._model
        model.recording_changed_sig.connect(self._recording_received)
        view.recording_selected.connect(lambda path: model.change_recording(path))
        view.background_image_selected.connect(
            lambda path: model.change_background(path)
        )

    def _recording_received(self) -> None:
        rec = self._model.recording
        if rec is None:
            return

        graphics = self._view.graphics
        vis = self._vis_strat
        vis.setup_plot(graphics=graphics, recording=rec)
        vis.update()
