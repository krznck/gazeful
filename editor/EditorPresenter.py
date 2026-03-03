"""Presenter for the Editor page, coordinating UI settings and visualizations."""
import re
from pathlib import Path

from AppContext import AppContext
from processing.ingester import ingest_csv
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from pyqtgraph.exporters import ImageExporter
from pyqtgraph.exporters.SVGExporter import SVGExporter
from pyqtgraph.parametertree.Parameter import Parameter
from visuals.pages.presenters.PagePresenter import PagePresenter

from editor.EditorPage import EditorPage
from editor.ParameterCollection import ParameterCollection
from editor.parameters.base import PARAMS, ParameterEnum
from editor.visualization.generator import make_param, make_strategy
from editor.visualization.VisualizationStrategy import VisualizationStrategy

IMAGE_WIDTH = 2000


class EditorPresenter(PagePresenter[EditorPage]):
    """Presenter managing the Editor view and visualization lifecycle.

    This class coordinates the parameter tree, handles file importing/exporting,
    and manages the active visualization strategy.

    Attributes:
        _vis_strat: Current strategy for generating the visualization.
        _params: Collection of parameters for UI and strategy control.
        _root_param: The top-level parameter group for the tree view.
        _common_params: Long-lived parameters (e.g., global settings).
        _specific_params: Parameters specific to the active visualization strategy.
    """

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
        """Initializes the presenter and creates initial parameter groups.

        Args:
            view: The EditorPage view.
            context: Global application context.
        """
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
        """Initializes the view's component states."""
        v, p = self._view, self._params
        p.connect_tree(v.parameter_tree)

    def _connect_signals(self) -> None:
        """Connects signals from parameters and context to presenter slots."""
        p, c = self._params, self._context
        p.connect(ParameterEnum.GAZE_FILE, self._on_gaze_csv_selected)
        p.connect(ParameterEnum.VISUALIZATION, self._on_visualization_type_selected)

        p.connect(ParameterEnum.SAVE, self._on_export_clicked)

        def import_recording():
            """Slot for importing a new recording into the current visualization."""
            if not c.main_data:
                return
            vs, v = self._vis_strat, self._view
            vs.setup_plot(v.graphics, c.main_data)
            vs.update()

        c.main_data_changed.connect(import_recording)

    def _on_export_clicked(self, _) -> None:
        """Handles the export of the current visualization to an image file."""
        v, c = self._view, self._context

        if not c.main_data:
            return

        file_path, selected_filter = QFileDialog.getSaveFileName(
            v,
            "Save Figure As...",
            filter=("PNG Image (*.png);;" "JPEG Image (*.jpg);;" "SVG Image (*.svg);;"),
        )

        if not file_path:
            return
        path = Path(file_path)

        if path.suffix == "":
            match = re.search(r"\*\.(\w+)", selected_filter)
            if match:
                path = path.with_suffix("." + match.group(1))
            else:
                path = path.with_suffix(".png")  # fallback

        if path.suffix == ".svg":
            exporter = SVGExporter(v.graphics.scene())
        else:
            exporter = ImageExporter(v.graphics.scene())
            exporter.parameters()["width"] = IMAGE_WIDTH

        exporter.export(str(path))

    def _on_gaze_csv_selected(self, _, value) -> None:
        """Slot triggered when a new CSV file is chosen from the parameter tree."""
        v, c = self._view, self._context

        if value == "":
            QMessageBox.warning(v, "Import warning", "Empty selection")
            return

        image = c.main_data.screenshot if c.main_data else None
        recording = ingest_csv(Path(value))
        recording.screenshot = image
        c.main_data = recording

    def _on_visualization_type_selected(self, _, value) -> None:
        """Slot triggered when the visualization type parameter is changed.

        Updates the visualization strategy and refreshes specific parameters.
        """
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
