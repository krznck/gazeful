from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QVBoxLayout

from AppContext import AppContext
from processing.Definitions import Definitions
from visuals.assets.icon_selector import IconsEnum
from visuals.customized_widgets.BoundedTextbox import BoundedFloatTextbox
from visuals.customized_widgets.Header import Header
from visuals.pages.Page import Page

TITLE = "Definitions"
ICON = IconsEnum.BOOK_INFO

BLINKS_SECTION_HEADER = "Closures"
BLINK_SECTION_TEXTBOX_LABEL = "Blink threshhold: "

OCULOMOTOR_SECTION_HEADER = "Oculomotor behavior"
FIXATION_MINIMUM_DURATION_LABEL = "Fixation minimum duration: "
FIXATION_MAXIMUM_DISPERSION = "Fixation maximum dispersion (in pixels): "


class DefinitionsPage(Page):
    defs: Definitions

    blink_threshhold_label: QLabel

    def __init__(self, context: AppContext) -> None:
        self.defs = context.defs
        super().__init__(TITLE, context, ICON)

    def add_content(self) -> None:
        super().add_content()
        self.__init_blinks_section()
        self.__init_oculomotor_section()

    def __init_blinks_section(self) -> None:
        vbox = QVBoxLayout()
        vbox.addWidget(Header(BLINKS_SECTION_HEADER))

        textbox = BoundedFloatTextbox(0, 1000, self.defs.blink_threshhold_ms)
        hbox = generate_definition_item(
            BLINK_SECTION_TEXTBOX_LABEL,
            textbox,
            "ms",
        )

        vbox.addLayout(hbox)

        self._page_vbox.addLayout(vbox)

    def __init_oculomotor_section(self) -> None:
        vbox = QVBoxLayout()
        vbox.addWidget(Header(OCULOMOTOR_SECTION_HEADER))

        textbox = BoundedFloatTextbox(0, 5000, self.defs.fixation_min_duration_ms)
        hbox = generate_definition_item(
            FIXATION_MINIMUM_DURATION_LABEL,
            textbox,
            "ms",
        )
        vbox.addLayout(hbox)

        textbox = BoundedFloatTextbox(0, 1000, self.defs.fixation_max_dispersion_px)
        hbox = generate_definition_item(FIXATION_MAXIMUM_DISPERSION, textbox, "pixels")
        vbox.addLayout(hbox)

        self._page_vbox.addLayout(vbox)


def generate_definition_item(
    title: str, textbox: BoundedFloatTextbox, measurement: str
) -> QHBoxLayout:
    main_hbox = QHBoxLayout()
    main_hbox.addWidget(QLabel(title))

    value_hbox = QHBoxLayout()
    value_hbox.addWidget(textbox)
    type_label = QLabel(measurement)
    value_hbox.addWidget(type_label)

    main_hbox.addLayout(value_hbox)
    return main_hbox
