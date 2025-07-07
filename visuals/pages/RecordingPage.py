from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtCore import QTimer
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QCheckBox
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QSlider
from PyQt6.QtWidgets import QVBoxLayout

from AppContext import AppContext
from recording import validators as val
from recording.Recorder import file_already_saved
from recording.Recorder import Recorder
from recording.screenshots import shoot_screen
from visuals.assets.AudioEnum import AudioEnum
from visuals.assets.icon_selector import IconsEnum
from visuals.customized_widgets.CustomPushButton import CustomPushButton
from visuals.pages.Page import Page

ICON = IconsEnum.RECORD
TITLE = "Recording"

RECORD_TOGGLE_OFF_TEXT = "Start recording"
RECORD_TOGGLE_ON_TEXT = "Stop recording"
FILENAME_PLACEHOLDER_TEXT = "filename"
EXPLORER_DIALOG_TEXT = "Select Directory"


class RecordingPage(Page):
    recorder: Recorder

    record_toggle: QPushButton
    explorer_button: QPushButton
    filename_textbox: QLineEdit
    screenshot_checkbox: QCheckBox
    dir_path_label: QLabel

    filename: str
    delay: int
    endless: bool
    duration: int

    def __init__(self, context: AppContext) -> None:
        self.delay = 0
        self.endless = True
        self.duration = 3
        self.recorder = context.recorder
        self.dir_path_label = QLabel()  # NOTE: gotta instantiate this for the property
        self.dir_path = val.get_default_recording_dir()
        self.filename = f"recording-{val.iso_8601_time()}"
        super().__init__(TITLE, context, ICON)

    @property
    def dir_path(self) -> str:
        return self._dir_path

    @dir_path.setter
    def dir_path(self, value: str) -> None:
        pl = self.dir_path_label
        if pl:
            pl.setText(f"Path: {value}")

        self._dir_path = value

    def add_content(self) -> None:
        self._init_file_section()
        self._init_enable_section()
        self._init_delay_section()
        self._init_duration_section()
        self._init_screenshot_section()
        return super().add_content()

    def _init_file_section(self):
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        eb = self.explorer_button = CustomPushButton(EXPLORER_DIALOG_TEXT)
        eb.clicked.connect(self.on_explorer_button_click)
        hbox.addWidget(eb)
        pl = self.dir_path_label = QLabel(f"Path: {self.dir_path}")
        hbox.addWidget(pl)
        vbox.addLayout(hbox)

        hbox = QHBoxLayout()  # clear out
        fl = QLabel("Filename:")
        hbox.addWidget(fl)
        ft = self.filename_textbox = QLineEdit()
        ft.setPlaceholderText(FILENAME_PLACEHOLDER_TEXT)
        ft.setText(self.filename)
        ft.textChanged.connect(self.on_path_textbox_text_changed)
        hbox.addWidget(ft)
        vbox.addLayout(hbox)

        odb = CustomPushButton("Open directory")
        odb.clicked.connect(lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(self.dir_path)))
        vbox.addWidget(odb)

        self.page_vbox.addLayout(vbox)

    def _init_enable_section(self):
        hbox = QHBoxLayout()

        self.record_toggle = CustomPushButton(RECORD_TOGGLE_OFF_TEXT)
        self.record_toggle.setCheckable(True)
        # self.record_toggle.setEnabled(False)
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

    def _init_duration_section(self):
        vbox = QVBoxLayout()

        checkbox = QCheckBox("Limit recording duration")
        checkbox.setChecked(False)

        vbox.addWidget(checkbox)

        hbox = QHBoxLayout()
        label = QLabel("Recording duration")
        label.setEnabled(False)
        hbox.addWidget(label)
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(3)
        slider.setMaximum(120)
        slider.setEnabled(False)
        slider.setValue(self.duration)
        descriptor = QLabel(f"{slider.value()} s")
        descriptor.setEnabled(False)
        slider.valueChanged.connect(
            lambda: self.on_duration_slider_value_changed(slider, descriptor)
        )
        hbox.addWidget(descriptor)
        hbox.addWidget(slider)

        vbox.addLayout(hbox)

        checkbox.checkStateChanged.connect(
            lambda: self.on_duration_checkbox_state_changed(
                checkbox, slider, [label, descriptor]
            )
        )

        self.page_vbox.addLayout(vbox)

    def _init_screenshot_section(self):
        self.screenshot_checkbox = checkbox = QCheckBox(
            "Take screenshot when recording starts"
        )
        checkbox.setChecked(True)
        self.page_vbox.addWidget(checkbox)

    def on_duration_checkbox_state_changed(
        self, checkbox: QCheckBox, slider: QSlider, labels: list[QLabel]
    ):
        checked = checkbox.isChecked()
        checkbox.setChecked(checked)
        slider.setEnabled(checked)
        self.endless = not checked
        for label in labels:
            label.setEnabled(checked)

    def on_duration_slider_value_changed(self, slider: QSlider, descriptor: QLabel):
        val = slider.value()
        descriptor.setText(f"{val} s")
        self.duration = val
        pass

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
                    self.record_toggle.setEnabled(True)
                    self._begin_recording(path)
                    AudioEnum.PIP.value.play()

                self.record_toggle.setEnabled(False)
                QTimer.singleShot(delay, lambda: play())
            else:
                self._begin_recording(path)
        else:
            recorder.stop()

        self.record_toggle.setText(
            RECORD_TOGGLE_ON_TEXT if on else RECORD_TOGGLE_OFF_TEXT
        )
        self.filename_textbox.setEnabled(not on)
        # self.recording_delay_slider.setEnabled(not on)

    def on_explorer_button_click(self):
        selection = QFileDialog.getExistingDirectory(
            self, directory=self.dir_path, caption=EXPLORER_DIALOG_TEXT
        )
        if len(selection) > 0:
            self.dir_path = selection
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

    def _begin_recording(self, path: Path):
        if self.screenshot_checkbox.isChecked():
            shoot_screen(
                self.context.screen,
                (self.dir_path + "/" + self.filename + "_screenshot.png"),
            )

        recorder = self.recorder
        if self.endless:
            recorder.start(path)
            return

        rt = self.record_toggle

        def stop():
            recorder.stop()
            AudioEnum.PIP.value.play()
            rt.setEnabled(True)
            rt.setText(RECORD_TOGGLE_OFF_TEXT)
            rt.setChecked(False)
            self.filename_textbox.setEnabled(True)

        rt.setEnabled(False)
        recorder.start(path)
        QTimer.singleShot(self.duration * 1000, lambda: stop())
