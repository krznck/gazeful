from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QMessageBox, QVBoxLayout
from pyqtgraph.widgets.GraphicsLayoutWidget import GraphicsLayoutWidget
from AppContext import AppContext
from editor.CommonParameters import CommonParameterTree
from editor.EditorController import EditorController
from editor.GazeModel import GazeModel
from editor.HeatmapVisualizationStrategy import HeatmapVisualizationStrategy
from visuals.assets.icon_selector import IconsEnum
from visuals.pages.Page import Page


# TODO: Should this even have a dedicated section, as opposed to being in /visuals/pages?
# Really should consider the separation here.
class EditorPage(Page):
    _controller: EditorController

    _param_tree: CommonParameterTree
    _graphics: GraphicsLayoutWidget
    _hover_label: QLabel

    recording_selected = pyqtSignal(str)
    background_image_selected = pyqtSignal(str)

    def __init__(self, context: AppContext) -> None:
        super().__init__(title="Editor", context=context, icon=IconsEnum.MICROSCOPE)

        # WARN: It's stupid that the view is responsible for instantiating these.
        # But that's a function of how I created the Pages, with the base Page holding context.
        # Might be worth refactoring.
        model = GazeModel(context)
        vis_strat = HeatmapVisualizationStrategy()
        self._controller = EditorController(
            view=self, model=model, visualization_strategy=vis_strat
        )

        self._param_tree = CommonParameterTree()
        self._graphics = GraphicsLayoutWidget()
        self._hover_label = QLabel()
        self.page_vbox.addLayout(self._init_layout())
        self._init_interactions()

    @property
    def graphics(self) -> GraphicsLayoutWidget:
        return self._graphics

    def _init_layout(self) -> QHBoxLayout:
        pt, g, hl = self._param_tree, self._graphics, self._hover_label

        layout = QHBoxLayout()
        layout.addWidget(pt, stretch=1)

        font = QFont()
        font.setPointSize(18)
        hl.setFont(font)

        preview = QVBoxLayout()
        preview.addWidget(g)
        preview.addWidget(hl)

        layout.addLayout(preview, stretch=2)
        return layout

    def _init_interactions(self) -> None:
        pt = self._param_tree

        csv = pt.get_param("Gaze CSV")
        csv.sigValueChanged.connect(self._gaze_csv_selector_clicked)

        back = pt.get_param("Background Image")
        back.sigValueChanged.connect(self._background_image_selector_clicked)

    def _gaze_csv_selector_clicked(self, _, value) -> None:
        if value == "":
            QMessageBox.warning(self, "Import warning", "Empty selection")
            return

        self.recording_selected.emit(value)

    def _background_image_selector_clicked(self, _, value) -> None:
        if value == "":
            QMessageBox.warning(self, "Import warning", "Empty selection")

        self.background_image_selected.emit(value)
