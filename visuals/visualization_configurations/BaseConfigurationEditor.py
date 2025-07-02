from pathlib import Path
from typing import Generic
from typing import TypeVar

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QSlider
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget

from visualizing.configuration.BaseConfiguration import BaseConfiguration
from visuals.customized_widgets.BoundedTextbox import BoundedFloatTextbox
from visuals.customized_widgets.CustomPushButton import CustomPushButton

Configuration = TypeVar("Configuration", bound=BaseConfiguration)


class BaseConfigurationEditor(QWidget, Generic[Configuration]):
    image_path_label: QLabel

    configuration: Configuration
    window_vbox: QVBoxLayout
    opaqueness_slider: QSlider

    def __init__(self, configuration: Configuration) -> None:
        self.configuration = configuration
        super().__init__()
        self.setWindowTitle("Visualization configuration:")
        self.window_vbox = QVBoxLayout()
        self.add_content()
        self.window_vbox.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.window_vbox)

    def add_content(self) -> None:
        self._init_screen_dimensions_section()
        self._init_image_section()
        self._init_opaqueness_section()

    def _init_screen_dimensions_section(self):
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Screen dimensions:"))

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

    def _init_image_section(self):
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Background image:"))

        inner_hbox = QHBoxLayout()
        self.image_path_label = label = QLabel("no path selected")
        inner_hbox.addWidget(label)
        button = CustomPushButton("Select image")
        button.clicked.connect(self.on_image_selection_button_click)
        inner_hbox.addWidget(button)

        hbox.addLayout(inner_hbox)
        self.window_vbox.addLayout(hbox)

    def _init_opaqueness_section(self):
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Opaqueness:"))

        inner_hbox = QHBoxLayout()
        self.opaqueness_slider = slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setTickInterval(10)
        slider.setSingleStep(10)
        slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        slider.setValue(int(self.configuration.opaqueness.value * 100))
        slider.valueChanged.connect(self.on_opaqueness_slider_value_changed)
        self.opaqueness_label = label = QLabel(str(self.configuration.opaqueness.value))
        inner_hbox.addWidget(label)
        inner_hbox.addWidget(slider)

        hbox.addLayout(inner_hbox)

        self.window_vbox.addLayout(hbox)

    def on_image_selection_button_click(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select image",
            filter="Images (*.png *.jpg *.jpeg *.bmp *.webp)",
        )
        self.configuration.background_image.update(Path(path))
        self.image_path_label.setText(path)

    def on_opaqueness_slider_value_changed(self):
        self.configuration.opaqueness.update(self.opaqueness_slider.value() / 100)
        self.opaqueness_label.setText(str(self.configuration.opaqueness.value))
