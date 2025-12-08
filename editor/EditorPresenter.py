from pathlib import Path
from PyQt6.QtWidgets import QMessageBox
from pyqtgraph.parametertree.Parameter import Parameter
from AppContext import AppContext
from editor.EditorPage import EditorPage
from editor.ParameterCollection import ParameterCollection
from editor.visualization.VisualizationStrategy import VisualizationStrategy
from editor.visualization.generator import make_param, make_strategy
from processing.ingester import ingest_csv
from visuals.pages.presenters.PagePresenter import PagePresenter

from editor.parameters.base import PARAMS, ParameterEnum


class EditorPresenter(PagePresenter[EditorPage]):
    _vis_strat: VisualizationStrategy
    _params: ParameterCollection
    _root_param: Parameter  # container for the tree view
    _common_params: Parameter  # long-lived params
    _specific_params: Parameter | None  # disposable, specific params

    def __init__(
        self,
        view: EditorPage,
        context: AppContext,
    ) -> None:
        super().__init__(view, context)

        self._common_params = cp = Parameter.create(
            name="Common", type="group", children=PARAMS
        )
        self._specific_params = None
        self._root_param = rp = Parameter.create(
            name="params", type="group", children=[cp]
        )
        self._params = ParameterCollection(rp)

        self._init_view_state()
        self._connect_signals()

        initial_vis_type = self._params.get_value(ParameterEnum.VISUALIZATION)
        self._on_visualization_type_selected(None, initial_vis_type)

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
        if self._specific_params is not None:
            self._root_param.removeChild(self._specific_params)
            self._specific_params = None

        strat_type = make_strategy(value)
        self._specific_params = sp = Parameter.create(
            name="Specific", type="group", children=make_param(value)
        )

        if sp is not None:
            self._root_param.addChild(sp)

        self._vis_strat = strat_type(self._params)

        if recording := self._context.main_data:
            self._vis_strat.setup_plot(self._view.graphics, recording)
            self._vis_strat.update()
