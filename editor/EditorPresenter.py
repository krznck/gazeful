from pathlib import Path
from pyqtgraph.exporters import ImageExporter
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from pyqtgraph.parametertree.Parameter import Parameter
from AppContext import AppContext
from editor.EditorPage import EditorPage
from editor.ParameterCollection import ParameterCollection
from editor.visualization.VisualizationStrategy import VisualizationStrategy
from editor.visualization.generator import make_param, make_strategy
from processing.ingester import ingest_csv
from visuals.pages.presenters.PagePresenter import PagePresenter

from editor.parameters.base import PARAMS, ParameterEnum

IMAGE_WIDTH = 2000


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
        p, c = self._params, self._context
        p.connect(ParameterEnum.GAZE_FILE, self._on_gaze_csv_selected)
        p.connect(ParameterEnum.VISUALIZATION, self._on_visualization_type_selected)

        p.connect(ParameterEnum.SAVE, self._on_export_clicked)

        def import_recording():
            if not c.main_data:
                return
            vs, v = self._vis_strat, self._view
            vs.setup_plot(v.graphics, c.main_data)
            vs.update()

        c.main_data_changed.connect(import_recording)

    def _on_export_clicked(self, _) -> None:
        v, c = self._view, self._context

        if not c.main_data:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            v,
            "Save Figure As...",
            filter=("PNG Image (*.png);;" "JPEG Image (*jpg);;"),
        )
        if not file_path.endswith((".jpg", ".png")):
            file_path += ".png"

        exporter = ImageExporter(v.graphics.scene())
        exporter.parameters()["width"] = IMAGE_WIDTH
        exporter.export(file_path)

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
        self._vis_strat.hovered.connect(self._view.hover_label.setText)

        if recording := self._context.main_data:
            self._vis_strat.setup_plot(self._view.graphics, recording)
            self._vis_strat.update()
