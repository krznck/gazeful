"""The page for configuring the appearance of the real-time gaze visualizer."""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSlider

from visuals.assets.icon_selector import IconsEnum
from visuals.customized_widgets.CustomPushButton import CustomPushButton
from visuals.pages.Page import Page
from visuals.visualizer.constants import OPACITY
from visuals.visualizer.GazeVisualizer import GazeVisualizer

OPACITY_LABEL_TEXT: str = "Opacity: "


class VisualizerPage(Page):
    """The page used for controlling visualizer animations and transparency.

    Attributes:
        visualizer: Reference to the visualizer widget.
        animation_toggle: Button to enable/disable visualizer animations.
        opacity_slider: Slider to adjust the visualizer's opacity.
    """

    visualizer: GazeVisualizer

    animation_toggle: QPushButton
    opacity_slider: QSlider

    def __init__(self) -> None:
        """Initializes the visualizer page."""
        super().__init__("Visualizer", IconsEnum.CIRCLE)

    def add_content(self) -> None:
        """Adds page content, including animation and opacity sections."""
        super().add_content()
        self.__init_animation_section()
        self.__init_opacity_section()

    def __init_animation_section(self):
        """Initializes the visualizer animation toggle button."""
        hbox = QHBoxLayout()

        self.animation_toggle = CustomPushButton("Animations: On")
        self.animation_toggle.setCheckable(True)
        self.animation_toggle.setChecked(True)
        hbox.addWidget(self.animation_toggle)

        self._page_vbox.addLayout(hbox)

    def __init_opacity_section(self):
        """Initializes the slider for adjusting visualizer opacity."""
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
