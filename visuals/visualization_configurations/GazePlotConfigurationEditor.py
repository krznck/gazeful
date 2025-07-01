from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel

from visualizing.configuration.GazePlotConfiguration import GazePlotConfiguration
from visuals.customized_widgets.BoundedTextbox import BoundedFloatTextbox
from visuals.visualization_configurations.BaseConfigurationEditor import (
    BaseConfigurationEditor,
)


class GazePlotConfigurationEditor(BaseConfigurationEditor):
    configuration: GazePlotConfiguration

    def __init__(self, configuration: GazePlotConfiguration) -> None:
        super().__init__(configuration)

    def add_content(self) -> None:
        super().add_content()
        self._init_size_mulitplier_section()

    def _init_size_mulitplier_section(self) -> None:
        hbox = QHBoxLayout()

        hbox.addWidget(QLabel("Point size multiplier"))
        hbox.addWidget(
            BoundedFloatTextbox(10, 10000, binding=self.configuration.size_multiplier)
        )

        self.window_vbox.addLayout(hbox)
