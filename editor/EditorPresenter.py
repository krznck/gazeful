from pathlib import Path
from PyQt6.QtWidgets import QMessageBox
from AppContext import AppContext
from editor.EditorPage import EditorPage
from editor.HeatmapVisualizationStrategy import HeatmapVisualizationStrategy
from editor.ParameterCollection import ParameterCollection, ParameterEnum
from editor.VisualizationStrategy import VisualizationStrategy
from processing.ingester import ingest_csv
from visuals.pages.presenters.PagePresenter import PagePresenter


class EditorPresenter(PagePresenter[EditorPage]):
    _vis_strat: VisualizationStrategy
    _params: ParameterCollection

    def __init__(
        self,
        view: EditorPage,
        context: AppContext,
        visualization_strategy: VisualizationStrategy | None = None,
    ) -> None:
        super().__init__(view, context)
        self._params = ParameterCollection()

        if visualization_strategy:
            self._vis_strat = visualization_strategy
        else:
            default = HeatmapVisualizationStrategy(parameters=self._params)
            self._vis_strat = default

        self._init_view_state()
        self._connect_signals()

    def _init_view_state(self) -> None:
        v, p = self._view, self._params
        p.connect_tree(v.parameter_tree)

    def _connect_signals(self) -> None:
        p = self._params
        p.connect(ParameterEnum.GAZE_FILE, self._on_gaze_csv_selected)

    def _on_gaze_csv_selected(self, _, value) -> None:
        v, c, vs = self._view, self._context, self._vis_strat

        if value == "":
            QMessageBox.warning(v, "Import warning", "Empty selection")
            return

        recording = ingest_csv(Path(value))
        c.main_data = recording
        vs.setup_plot(v.graphics, recording)
        vs.update()
