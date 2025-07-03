from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtCore import QTimer
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QSlider

from AppContext import AppContext
from recording import validators as val
from recording.Recorder import file_already_saved
from recording.Recorder import Recorder
from visuals.assets.AudioEnum import AudioEnum
from visuals.assets.icon_selector import IconsEnum
from visuals.customized_widgets.CustomPushButton import CustomPushButton
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
    delay: int
    record_sound: QSoundEffect

    def __init__(self, context: AppContext) -> None:
        super().__init__(TITLE, context, ICON)
        self.recorder = self.context.recorder
        self.delay = 0

    def add_content(self) -> None:
        self._init_file_section()
        self._init_enable_section()
        self._init_delay_section()
        return super().add_content()

    def _init_file_section(self):
        hbox = QHBoxLayout()

        self.explorer_button = CustomPushButton(EXPLORER_DIALOG_TEXT)
        self.explorer_button.clicked.connect(self.on_explorer_button_click)
        hbox.addWidget(self.explorer_button)

        self.filename_textbox = QLineEdit()
        self.filename_textbox.setPlaceholderText(FILENAME_PLACEHOLDER_TEXT)
        self.filename_textbox.textChanged.connect(self.on_path_textbox_text_changed)
        hbox.addWidget(self.filename_textbox)

        self.page_vbox.addLayout(hbox)

    def _init_enable_section(self):
        hbox = QHBoxLayout()

        self.record_toggle = CustomPushButton(RECORD_TOGGLE_OFF_TEXT)
        self.record_toggle.setCheckable(True)
        self.record_toggle.setEnabled(False)
        self.record_toggle.clicked.connect(self.on_record_toggle_click)

        hbox.addWidget(self.record_toggle)

        self.page_vbox.addLayout(hbox)

    def _init_delay_section(self):
        hbox = QHBoxLayout()

        hbox.addWidget(QLabel("Delay before recording"))

        self.recording_delay_slider = slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(120)
        # slider.setTickInterval(1)
        # slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        slider.setValue(0)
        hbox.addWidget(slider)

        self.recording_delay_value_label = vl = QLabel(f"{slider.value()} s")
        hbox.addWidget(vl)

        slider.valueChanged.connect(self.on_recording_delay_slider_value_changed)

        self.page_vbox.addLayout(hbox)

    def on_recording_delay_slider_value_changed(self):
        label = self.recording_delay_value_label
        slider = self.recording_delay_slider
        val = slider.value()
        label.setText(f"{val} s")
        self.delay = val

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

        if on:
            delay = self.delay * 1000  # seconds to miliseconds
            if delay > 0:

                def play():
                    recorder.start(path)
                    AudioEnum.PIP.value.play()
                    self.record_toggle.setEnabled(True)

                self.record_toggle.setEnabled(False)
                QTimer.singleShot(delay, lambda: play())
            else:
                recorder.start(path)
        else:
            recorder.stop()

        self.record_toggle.setText(
            RECORD_TOGGLE_ON_TEXT if on else RECORD_TOGGLE_OFF_TEXT
        )
        self.filename_textbox.setEnabled(not on)
        self.recording_delay_slider.setEnabled(not on)

    def on_explorer_button_click(self):
        self.dir_path = QFileDialog.getExistingDirectory(self, EXPLORER_DIALOG_TEXT)
        self._check_path()

    def on_path_textbox_text_changed(self):
        self.filename = self.filename_textbox.text()
        self._check_path()

    def _confirm_overwrite(self, path: Path) -> bool:
        reply = QMessageBox.question(
            self,
            "File Exists",
            f"The file '{path.name}' already exists. Do you want to overwrite to it?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        return reply == QMessageBox.StandardButton.Yes
