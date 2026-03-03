"""View component for the Editor page."""
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout
from pyqtgraph.parametertree import ParameterTree
from pyqtgraph.widgets.GraphicsLayoutWidget import GraphicsLayoutWidget
from visuals.assets.icon_selector import IconsEnum
from visuals.pages.Page import Page


class EditorPage(Page):
    """The UI page for the visualization editor.

    Displays a parameter tree for settings on the left and a large graphics
    preview on the right.

    Attributes:
        graphics: The main visualization display area.
        hover_label: Label for displaying information about hovered elements.
        parameter_tree: The settings pane for visual configuration.
    """

    graphics: GraphicsLayoutWidget
    hover_label: QLabel
    parameter_tree: ParameterTree

    def __init__(self) -> None:
        """Initializes the editor page view."""
        self.hover_label = QLabel()
        super().__init__(title="Editor", icon=IconsEnum.MICROSCOPE)

    def add_content(self) -> None:
        """Adds the layout and widgets to the page."""
        self._init_layout()

    def _init_layout(self) -> None:
        """Sets up the split layout between parameters and preview."""
        layout = QHBoxLayout()
        self.parameter_tree = pt = ParameterTree()
        layout.addWidget(pt, stretch=1)

        font = QFont()
        font.setPointSize(18)
        hl = self.hover_label
        hl.setFont(font)

        preview = QVBoxLayout()
        self.graphics = g = GraphicsLayoutWidget()
        preview.addWidget(g)
        preview.addWidget(hl)

        layout.addLayout(preview, stretch=2)
        self._page_vbox.addLayout(layout)
