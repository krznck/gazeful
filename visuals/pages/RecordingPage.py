from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QPushButton

from AppContext import AppContext
from Recorder import Recorder
from visuals.customized_widgets.CustomPushButton import CustomPushButton
from visuals.icons.icon_selector import IconsEnum
from visuals.pages.Page import Page

ICON = IconsEnum.RECORD
TITLE = "Recording"


class RecordingPage(Page):
    recorder: Recorder

    record_toggle: QPushButton

    def __init__(self, context: AppContext) -> None:
        super().__init__(TITLE, context, ICON)
        self.recorder = self.context.recorder

    def add_content(self) -> None:
        self.__init_enable_section()
        return super().add_content()

    def __init_enable_section(self):
        hbox = QHBoxLayout()

        # ISSUE: This is only a temporary solution ot see that recording works.
        self.record_toggle = CustomPushButton("Start recording")
        self.record_toggle.setCheckable(True)
        self.record_toggle.clicked.connect(self.on_record_toggle_click)

        hbox.addWidget(self.record_toggle)

        self.page_vbox.addLayout(hbox)

    def on_record_toggle_click(self):
        recorder = self.recorder
        recorder.start() if self.record_toggle.isChecked() else recorder.stop()
