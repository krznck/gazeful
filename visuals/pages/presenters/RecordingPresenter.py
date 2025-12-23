from pathlib import Path

from PyQt6.QtCore import QTimer, QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QFileDialog, QMessageBox

from AppContext import AppContext
from recording import validators as val
from recording.Recorder import file_already_saved
from visuals.assets.AudioEnum import AudioEnum
from visuals.pages.RecordingPage import (
    EXPLORER_DIALOG_TEXT,
    RECORD_TOGGLE_OFF_TEXT,
    RECORD_TOGGLE_ON_TEXT,
    RecordingPage,
)
from visuals.pages.presenters.PagePresenter import PagePresenter


class RecordingPresenter(PagePresenter[RecordingPage]):
    _delay: int = 0
    _endless: bool = True
    _duration: int = 3
    _dir_path: str
    _filename: str

    def __init__(self, view: RecordingPage, context: AppContext) -> None:
        super().__init__(view, context)
        self._init_state()
        self._init_view_state()
        self._connect_signals()
        self._check_path()

    def _init_state(self):
        self._dir_path = str(
            val.get_default_recording_dir() / f"gaze-session-{val.iso_8601_date()}"
        )
        self._filename = f"recording-{val.iso_8601_time()}"

    def _init_view_state(self):
        v = self._view
        v.dir_path_label.setText(f"Path: {self._dir_path}")
        v.filename_textbox.setText(self._filename)

    def _connect_signals(self):
        v = self._view
        v.explorer_button.clicked.connect(self._on_explorer_button_click)
        v.filename_textbox.textChanged.connect(self._on_path_textbox_text_changed)
        v.open_dir_button.clicked.connect(self._on_open_dir_button_clicked)
        v.record_toggle.clicked.connect(self._on_record_toggle_click)
        v.recording_delay_slider.valueChanged.connect(
            self._on_recording_delay_slider_value_changed
        )
        v.duration_checkbox.stateChanged.connect(
            self._on_duration_checkbox_state_changed
        )
        v.duration_slider.valueChanged.connect(self._on_duration_slider_value_changed)

    def _on_duration_checkbox_state_changed(self):
        v = self._view
        checked = v.duration_checkbox.isChecked()
        v.duration_slider.setEnabled(checked)
        self._endless = not checked
        v.duration_label.setEnabled(checked)
        v.duration_descriptor.setEnabled(checked)

    def _on_duration_slider_value_changed(self):
        v = self._view
        val = v.duration_slider.value()
        v.duration_descriptor.setText(f"{val} s")
        self._duration = val

    def _on_recording_delay_slider_value_changed(self):
        v = self._view
        val = v.recording_delay_slider.value()
        v.recording_delay_value_label.setText(f"{val} s")
        self._delay = val

    def _check_path(self):
        ok = val.is_valid_dir(self._dir_path) and val.is_valid_filename(self._filename)
        self._view.record_toggle.setEnabled(ok)

    def _on_record_toggle_click(self):
        v, c = self._view, self._context
        on = v.record_toggle.isChecked()
        path = Path(self._dir_path, self._filename)
        if on and file_already_saved(path) and not self._confirm_overwrite(path):
            v.record_toggle.setChecked(False)
            return

        if on:
            delay = self._delay * 1000  # seconds to miliseconds
            if delay > 0:

                def play():
                    v.record_toggle.setEnabled(True)
                    self._begin_recording(path)
                    AudioEnum.PIP.value.play()

                v.record_toggle.setEnabled(False)
                QTimer.singleShot(delay, play)
            else:
                self._begin_recording(path)
        else:
            c.main_data = c.recorder.stop()

        v.record_toggle.setText(RECORD_TOGGLE_ON_TEXT if on else RECORD_TOGGLE_OFF_TEXT)
        v.filename_textbox.setEnabled(not on)

    def _on_explorer_button_click(self):
        selection = QFileDialog.getExistingDirectory(
            self._view, directory=self._dir_path, caption=EXPLORER_DIALOG_TEXT
        )
        if len(selection) > 0:
            self._dir_path = selection
            self._view.dir_path_label.setText(f"Path: {self._dir_path}")
            self._check_path()

    def _on_open_dir_button_clicked(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile(self._dir_path))

    def _on_path_textbox_text_changed(self):
        self._filename = self._view.filename_textbox.text()
        self._check_path()

    def _confirm_overwrite(self, path: Path) -> bool:
        reply = QMessageBox.question(
            self._view,
            "File Exists",
            f"The file '{path.name}' already exists. Do you want to overwrite to it?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        return reply == QMessageBox.StandardButton.Yes

    def _begin_recording(self, path: Path):
        v, c = self._view, self._context
        screen = (
            c.tracked_screen
            if v.screenshot_checkbox and v.screenshot_checkbox.isChecked()
            else None
        )

        recorder = c.recorder
        if self._endless:
            recorder.start(path=path, screenshot_screen=screen)
            return

        rt = v.record_toggle

        def stop():
            c.main_data = recorder.stop()
            AudioEnum.PIP.value.play()
            rt.setEnabled(True)
            rt.setText(RECORD_TOGGLE_OFF_TEXT)
            rt.setChecked(False)
            v.filename_textbox.setEnabled(True)

        rt.setEnabled(False)
        recorder.start(path=path, screenshot_screen=screen)
        QTimer.singleShot(self._duration * 1000, stop)
