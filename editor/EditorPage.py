from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout
from pyqtgraph.widgets.GraphicsLayoutWidget import GraphicsLayoutWidget
from AppContext import AppContext
from editor.CommonParameters import CommonParameterTree
from processing.GazeRecording import GazeRecording
from visuals.pages.Page import Page


# TODO: Should this even have a dedicated section, as opposed to being in /visuals/pages?
# Really should consider the separation here.
class EditorPage(Page):
    _recording: GazeRecording
    _param_tree: CommonParameterTree
    _graphics: GraphicsLayoutWidget
    _hover_label: QLabel

    def __init__(self, context: AppContext) -> None:
        super().__init__(title="Editor", context=context)
        # self._recording = recording # TODO: add recording detection
        # NOTE: I guess that's a behavior thing though. Maybe seperating behavior and
        # appearance would be good here, haven't been too good with that so far.
        self._param_tree = CommonParameterTree()
        self._graphics = GraphicsLayoutWidget()
        self._hover_label = QLabel()
        self.page_vbox.addLayout(self._init_layout())

    def _init_layout(self) -> QHBoxLayout:
        pt, g, hl = self._param_tree, self._graphics, self._hover_label

        layout = QHBoxLayout()
        layout.addWidget(pt, stretch=1)

        hl.setText("no information")
        font = QFont()
        font.setPointSize(18)
        hl.setFont(font)

        preview = QVBoxLayout()
        preview.addWidget(g)
        preview.addWidget(hl)

        layout.addLayout(preview, stretch=2)
        return layout
