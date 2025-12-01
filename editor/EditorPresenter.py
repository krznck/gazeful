from pathlib import Path
from PyQt6.QtWidgets import QMessageBox
from AppContext import AppContext
from editor.EditorPage import EditorPage
from editor.ParameterCollection import ParameterCollection, ParameterEnum
from editor.visualization.HeatmapVisualizationStrategy import (
    HeatmapVisualizationStrategy,
)
from editor.visualization.VisualizationStrategy import VisualizationStrategy
from editor.visualization.generator import make_strategy
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
        p.connect(ParameterEnum.VISUALIZATION, self._on_visualization_type_selected)

    def _on_gaze_csv_selected(self, _, value) -> None:
        v, c, vs = self._view, self._context, self._vis_strat

        if value == "":
            QMessageBox.warning(v, "Import warning", "Empty selection")
            return

        recording = ingest_csv(Path(value))
        c.main_data = recording
        vs.setup_plot(v.graphics, recording)
        vs.update()

    def _on_visualization_type_selected(self, _, value) -> None:
        strat = make_strategy(value)
        self._vis_strat = strat(self._params)

        v, c, vs = self._view, self._context, self._vis_strat

        if recording := c.main_data:
            vs.setup_plot(graphics=v.graphics, recording=recording)
            vs.update()
