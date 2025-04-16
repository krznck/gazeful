import os
from pathlib import Path

from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QPushButton

from AppContext import AppContext
from Recorder import Recorder
from visuals.customized_widgets.CustomPushButton import CustomPushButton
from visuals.icons.icon_selector import IconsEnum
from visuals.pages.Page import Page

ICON = IconsEnum.RECORD
TITLE = "Recording"

RECORD_TOGGLE_OFF_TEXT = "Start recording"
RECORD_TOGGLE_ON_TEXT = "Stop recording"
EXPLORER_BUTTON_TEXT = "Choose location"
PATH_PLACEHOLDER_TEXT = "gaze data path"
PATH_MINIMUM_WIDTH = 200

EXPLORER_DIALOG_TEXT = "Select Directory"


class RecordingPage(Page):
    recorder: Recorder

    record_toggle: QPushButton
    explorer_button: QPushButton
    path_textbox: QLineEdit

    def __init__(self, context: AppContext) -> None:
        super().__init__(TITLE, context, ICON)
        self.recorder = self.context.recorder

    def add_content(self) -> None:
        self.__init_file_section()
        self.__init_enable_section()
        return super().add_content()

    def __init_file_section(self):
        hbox = QHBoxLayout()

        self.explorer_button = CustomPushButton(EXPLORER_BUTTON_TEXT)
        self.explorer_button.clicked.connect(self.on_explorer_button_click)
        hbox.addWidget(self.explorer_button)

        self.path_textbox = QLineEdit()
        self.path_textbox.setPlaceholderText(PATH_PLACEHOLDER_TEXT)
        self.path_textbox.setMinimumWidth(PATH_MINIMUM_WIDTH)
        self.path_textbox.textChanged.connect(self.on_path_textbox_text_changed)
        hbox.addWidget(self.path_textbox)

        self.page_vbox.addLayout(hbox)

    def __init_enable_section(self):
        hbox = QHBoxLayout()

        self.record_toggle = CustomPushButton(RECORD_TOGGLE_OFF_TEXT)
        self.record_toggle.setCheckable(True)
        self.record_toggle.setEnabled(False)
        self.record_toggle.clicked.connect(self.on_record_toggle_click)

        hbox.addWidget(self.record_toggle)

        self.page_vbox.addLayout(hbox)

    def on_record_toggle_click(self):
        on = self.record_toggle.isChecked()
        recorder = self.recorder
        recorder.start(self.path_textbox.text()) if on else recorder.stop()
        self.record_toggle.setText(
            RECORD_TOGGLE_ON_TEXT if on else RECORD_TOGGLE_OFF_TEXT
        )
        self.path_textbox.setEnabled(not on)

    def on_explorer_button_click(self):
        directory = QFileDialog.getExistingDirectory(self, EXPLORER_DIALOG_TEXT)
        self.path_textbox.setText(directory)

    def on_path_textbox_text_changed(self):
        valid = is_valid_writeable_path(self.path_textbox.text())
        self.record_toggle.setEnabled(valid)


def is_valid_writeable_path(file_path: str):
    path = Path(file_path)
    if not path.is_absolute() or path.is_dir():
        return False
    parent_dir = path.parent
    return (
        parent_dir.exists() and parent_dir.is_dir() and os.access(parent_dir, os.W_OK)
    )
