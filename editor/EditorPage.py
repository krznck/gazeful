from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout
from pyqtgraph.parametertree import ParameterTree
from pyqtgraph.widgets.GraphicsLayoutWidget import GraphicsLayoutWidget
from visuals.assets.icon_selector import IconsEnum
from visuals.pages.Page import Page


# TODO: Should this even have a dedicated section, as opposed to being in /visuals/pages?
# Really should consider the separation here.
class EditorPage(Page):
    graphics: GraphicsLayoutWidget
    hover_label: QLabel
    parameter_tree: ParameterTree

    recording_selected = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__(title="Editor", icon=IconsEnum.MICROSCOPE)
        self.hover_label = QLabel()

    def add_content(self) -> None:
        self._init_layout()

    def _init_layout(self) -> None:
        layout = QHBoxLayout()
        self.parameter_tree = pt = ParameterTree()
        layout.addWidget(pt, stretch=1)

        font = QFont()
        font.setPointSize(18)
        self.hover_label = hl = QLabel()
        hl.setFont(font)

        preview = QVBoxLayout()
        self.graphics = g = GraphicsLayoutWidget()
        preview.addWidget(g)
        preview.addWidget(hl)

        layout.addLayout(preview, stretch=2)
        self._page_vbox.addLayout(layout)
