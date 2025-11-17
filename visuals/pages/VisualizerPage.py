from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QSlider

from visuals.assets.icon_selector import IconsEnum
from visuals.customized_widgets.CustomPushButton import CustomPushButton
from visuals.pages.Page import Page
from visuals.visualizer.constants import OPACITY
from visuals.visualizer.GazeVisualizer import GazeVisualizer

OPACITY_LABEL_TEXT: str = "Opacity: "


class VisualizerPage(Page):
    visualizer: GazeVisualizer

    animation_toggle: QPushButton
    opacity_slider: QSlider

    def __init__(self) -> None:
        super().__init__("Visualizer", IconsEnum.CIRCLE)

    def add_content(self) -> None:
        super().add_content()
        self.__init_animation_section()
        self.__init_opacity_section()

    def __init_animation_section(self):
        hbox = QHBoxLayout()

        self.animation_toggle = CustomPushButton("Animations: On")
        self.animation_toggle.setCheckable(True)
        self.animation_toggle.setChecked(True)
        hbox.addWidget(self.animation_toggle)

        self._page_vbox.addLayout(hbox)

    def __init_opacity_section(self):
        hbox = QHBoxLayout()

        label = QLabel(OPACITY_LABEL_TEXT)
        hbox.addWidget(label)

        self.opacity_slider = slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(255)
        slider.setValue(OPACITY)
        slider.setTickInterval(15)
        slider.setSingleStep(15)
        slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        hbox.addWidget(self.opacity_slider)

        self._page_vbox.addLayout(hbox)
