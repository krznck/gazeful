from pathlib import Path

from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QPushButton

from AppContext import AppContext
from recording import validators as val
from recording.Recorder import file_already_saved
from recording.Recorder import Recorder
from visuals.customized_widgets.CustomPushButton import CustomPushButton
from visuals.icons.icon_selector import IconsEnum
from visuals.pages.Page import Page

ICON = IconsEnum.RECORD
TITLE = "Recording"

RECORD_TOGGLE_OFF_TEXT = "Start recording"
RECORD_TOGGLE_ON_TEXT = "Stop recording"
FILENAME_PLACEHOLDER_TEXT = "data"
EXPLORER_DIALOG_TEXT = "Select Directory"


class RecordingPage(Page):
    recorder: Recorder

    record_toggle: QPushButton
    explorer_button: QPushButton
    filename_textbox: QLineEdit

    dir_path: str = ""
    filename: str = ""

    def __init__(self, context: AppContext) -> None:
        super().__init__(TITLE, context, ICON)
        self.recorder = self.context.recorder

    def add_content(self) -> None:
        self.__init_file_section()
        self.__init_enable_section()
        return super().add_content()

    def __init_file_section(self):
        hbox = QHBoxLayout()

        self.explorer_button = CustomPushButton(EXPLORER_DIALOG_TEXT)
        self.explorer_button.clicked.connect(self.on_explorer_button_click)
        hbox.addWidget(self.explorer_button)

        self.filename_textbox = QLineEdit()
        self.filename_textbox.setPlaceholderText(FILENAME_PLACEHOLDER_TEXT)
        self.filename_textbox.textChanged.connect(self.on_path_textbox_text_changed)
        hbox.addWidget(self.filename_textbox)

        self.page_vbox.addLayout(hbox)

    def __init_enable_section(self):
        hbox = QHBoxLayout()

        self.record_toggle = CustomPushButton(RECORD_TOGGLE_OFF_TEXT)
        self.record_toggle.setCheckable(True)
        self.record_toggle.setEnabled(False)
        self.record_toggle.clicked.connect(self.on_record_toggle_click)

        hbox.addWidget(self.record_toggle)

        self.page_vbox.addLayout(hbox)

    def _check_path(self):
        ok = val.is_valid_dir(self.dir_path) and val.is_valid_filename(self.filename)
        self.record_toggle.setEnabled(ok)

    def on_record_toggle_click(self):
        on = self.record_toggle.isChecked()
        recorder = self.recorder
        path = Path(self.dir_path, self.filename)
        if on and file_already_saved(path) and not self._confirm_overwrite(path):
            self.record_toggle.setChecked(False)
            return

        recorder.start(path) if on else recorder.stop()
        self.record_toggle.setText(
            RECORD_TOGGLE_ON_TEXT if on else RECORD_TOGGLE_OFF_TEXT
        )
        self.filename_textbox.setEnabled(not on)

    def on_explorer_button_click(self):
        self.dir_path = QFileDialog.getExistingDirectory(self, EXPLORER_DIALOG_TEXT)
        self._check_path()

    def on_path_textbox_text_changed(self):
        self.filename = self.filename_textbox.text()
        self._check_path()

    # TODO: Change to overwrite completely, rather than append
    def _confirm_overwrite(self, path: Path) -> bool:
        reply = QMessageBox.question(
            self,
            "File Exists",
            f"The file '{path.name}' already exists. Do you want to append to it?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        return reply == QMessageBox.StandardButton.Yes
