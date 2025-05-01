from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QSlider
from PyQt6.QtWidgets import QVBoxLayout

from AppContext import AppContext
from processing.Definitions import Definitions
from visuals.customized_widgets.Header import Header
from visuals.icons.icon_selector import IconsEnum
from visuals.pages.Page import Page

TITLE = "Definitions"
ICON = IconsEnum.BOOK_INFO

BLINKS_SECTION_HEADER = "Blinks"
BLINK_SECTION_SLIDER_LABEL = "Blink threshhold: "


class DefinitionsPage(Page):
    defs: Definitions

    blink_threshhold_slider: QSlider
    blink_threshhold_label: QLabel

    def __init__(self, context: AppContext) -> None:
        self.defs = context.defs
        super().__init__(TITLE, context, ICON)

    def add_content(self) -> None:
        super().add_content()
        self.__init_blinks_section()

    def __init_blinks_section(self) -> None:
        pass
        vbox = QVBoxLayout()
        vbox.addWidget(Header(BLINKS_SECTION_HEADER))

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(BLINK_SECTION_SLIDER_LABEL))

        # TODO: Consider these parameters more carefully, unsure of how sane they are
        self.blink_threshhold_slider = QSlider(Qt.Orientation.Horizontal)
        self.blink_threshhold_slider.setMinimum(0)
        self.blink_threshhold_slider.setMaximum(1000)
        self.blink_threshhold_slider.setTickInterval(10)
        self.blink_threshhold_slider.setValue(int(self.defs.blink_treshhold_ms))
        self.blink_threshhold_slider.valueChanged.connect(
            self.on_blink_threshhold_slider_valueChanged
        )
        hbox.addWidget(self.blink_threshhold_slider)

        self.blink_threshhold_label = QLabel(
            f"{str(self.blink_threshhold_slider.value())} ms"
        )
        hbox.addWidget(self.blink_threshhold_label)

        vbox.addLayout(hbox)

        self.page_vbox.addLayout(vbox)

    def on_blink_threshhold_slider_valueChanged(self) -> None:
        val = self.blink_threshhold_slider.value()
        self.defs.blink_treshhold_ms = val
        self.blink_threshhold_label.setText(str(val))
        print(self.defs.blink_treshhold_ms)
