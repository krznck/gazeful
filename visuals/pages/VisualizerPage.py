from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QSlider

from AppContext import AppContext
from visuals.customized_widgets.CustomPushButton import CustomPushButton
from visuals.icons.icon_selector import IconsEnum
from visuals.pages.Page import Page
from visuals.visualizer.constants import OPACITY
from visuals.visualizer.GazeVisualizer import GazeVisualizer

TITLE = "Visualizer"
ICON = IconsEnum.CIRCLE
LAYOUT_ALLIGNMENT: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignTop

ANIMATION_TOGGLE_ON_TEXT: str = "Animations: On"
ANIMATION_TOGGLE_OFF_TEXT: str = "Animations: Off"

OPACITY_LABEL_TEXT: str = "Opacity: "


class VisualizerPage(Page):
    visualizer: GazeVisualizer

    animation_toggle: QPushButton
    opacity_slider: QSlider

    def __init__(self, context: AppContext) -> None:
        super().__init__(TITLE, context, ICON)
        self.visualizer = self.context.visualizer

    def add_content(self) -> None:
        super().add_content()
        self.__init_animation_section()
        self.__init_opacity_section()

    def __init_animation_section(self):
        hbox = QHBoxLayout()

        self.animation_toggle = CustomPushButton(ANIMATION_TOGGLE_ON_TEXT)
        self.animation_toggle.setCheckable(True)
        self.animation_toggle.setChecked(True)
        self.animation_toggle.clicked.connect(self.on_animation_toggle_click)

        hbox.addWidget(self.animation_toggle)

        self.page_vbox.addLayout(hbox)

    def __init_opacity_section(self):
        hbox = QHBoxLayout()

        label = QLabel(OPACITY_LABEL_TEXT)
        hbox.addWidget(label)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(255)
        self.slider.setValue(OPACITY)
        self.slider.setTickInterval(15)
        self.slider.valueChanged.connect(self.on_opacity_slider_value_changed)

        hbox.addWidget(self.slider)

        self.page_vbox.addLayout(hbox)

    def on_animation_toggle_click(self):
        on = self.animation_toggle.isChecked()
        text = ANIMATION_TOGGLE_ON_TEXT if on else ANIMATION_TOGGLE_OFF_TEXT
        self.animation_toggle.setText(text)
        self.visualizer.toggle_animations(on)

    def on_opacity_slider_value_changed(self):
        self.visualizer.set_opacity(self.slider.value())
