from typing import Generic
from typing import TypeVar

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget

from visualizing.configuration.BaseConfiguration import BaseConfiguration
from visuals.customized_widgets.BoundedTextbox import BoundedFloatTextbox
from visuals.customized_widgets.Header import Header

Configuration = TypeVar("Configuration", bound=BaseConfiguration)


class BaseConfigurationEditor(QWidget, Generic[Configuration]):
    configuration: Configuration
    window_vbox: QVBoxLayout

    def __init__(self, configuration: Configuration) -> None:
        self.configuration = configuration
        super().__init__()
        self.setWindowTitle("Visualization configuration")
        self.window_vbox = QVBoxLayout()
        self.add_content()
        self.window_vbox.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.window_vbox)

    def add_content(self) -> None:
        self._init_screen_dimensions_section()

    def _init_screen_dimensions_section(self):
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Screen dimensions"))

        inner_hbox = QHBoxLayout()
        # NOTE: 8K UHD resolution as max
        width_textbox = BoundedFloatTextbox(0, 7680, self.configuration.screen_width)
        x_label = QLabel("x")
        height_textbox = BoundedFloatTextbox(0, 4320, self.configuration.screen_height)
        inner_hbox.addWidget(width_textbox)
        inner_hbox.addWidget(x_label)
        inner_hbox.addWidget(height_textbox)

        hbox.addLayout(inner_hbox)
        self.window_vbox.addLayout(hbox)
