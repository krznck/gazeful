from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QMessageBox, QVBoxLayout
from pyqtgraph.parametertree import ParameterTree
from pyqtgraph.widgets.GraphicsLayoutWidget import GraphicsLayoutWidget
from AppContext import AppContext
from editor.EditorController import EditorController
from editor.GazeModel import GazeModel
from editor.HeatmapVisualizationStrategy import HeatmapVisualizationStrategy
from editor.ParameterCollection import ParameterCollection, ParameterEnum
from visuals.assets.icon_selector import IconsEnum
from visuals.pages.Page import Page


# TODO: Should this even have a dedicated section, as opposed to being in /visuals/pages?
# Really should consider the separation here.
class EditorPage(Page):
    _controller: EditorController

    _params: ParameterCollection
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

        self._params = ParameterCollection()
        self._graphics = GraphicsLayoutWidget()
        self._hover_label = QLabel()
        self.page_vbox.addLayout(self._init_layout())
        self._init_interactions()

    @property
    def graphics(self) -> GraphicsLayoutWidget:
        return self._graphics

    def _init_layout(self) -> QHBoxLayout:
        p, g, hl = self._params, self._graphics, self._hover_label

        layout = QHBoxLayout()
        pt = ParameterTree()
        p.connect_tree(pt)
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
        p = self._params

        p.connect(ParameterEnum.GAZE_FILE, self._gaze_csv_selector_clicked)
        p.connect(ParameterEnum.BACKGROUND, self._background_image_selector_clicked)

    def _gaze_csv_selector_clicked(self, _, value) -> None:
        if value == "":
            QMessageBox.warning(self, "Import warning", "Empty selection")
            return

        self.recording_selected.emit(value)

    def _background_image_selector_clicked(self, _, value) -> None:
        if value == "":
            QMessageBox.warning(self, "Import warning", "Empty selection")

        self.background_image_selected.emit(value)
