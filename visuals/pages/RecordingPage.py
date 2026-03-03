"""The page for configuring and executing gaze recordings."""
import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QCheckBox, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QSlider, QVBoxLayout)

from visuals.assets.icon_selector import IconsEnum
from visuals.customized_widgets.CustomPushButton import CustomPushButton
from visuals.pages.Page import Page

RECORD_TOGGLE_OFF_TEXT = "Start recording"
RECORD_TOGGLE_ON_TEXT = "Stop recording"
EXPLORER_DIALOG_TEXT = "Select Directory"


class RecordingPage(Page):
    """The page used for selecting file paths and starting/stopping recordings.

    Attributes:
        record_toggle: Button to start/stop the recording process.
        explorer_button: Button to open a directory selection dialog.
        open_dir_button: Button to open the current recording directory in explorer.
        filename_textbox: Input field for the recording's filename.
        screenshot_checkbox: Checkbox to enable/disable initial screenshots.
        dir_path_label: Label showing the current recording directory.
        recording_delay_slider: Slider to set a delay before recording begins.
        duration_checkbox: Checkbox to enable fixed-duration recordings.
        duration_slider: Slider to set the fixed recording duration.
    """

    record_toggle: QPushButton
    explorer_button: QPushButton
    open_dir_button: QPushButton
    filename_textbox: QLineEdit
    screenshot_checkbox: QCheckBox | None
    dir_path_label: QLabel
    recording_delay_slider: QSlider
    recording_delay_value_label: QLabel
    duration_checkbox: QCheckBox
    duration_label: QLabel
    duration_slider: QSlider
    duration_descriptor: QLabel

    def __init__(self) -> None:
        """Initializes the recording page."""
        self.screenshot_checkbox = None
        super().__init__("Recording", IconsEnum.RECORD)

    def add_content(self) -> None:
        """Adds page content, including file, delay, and duration sections."""
        self._init_file_section()
        self._init_enable_section()
        self._init_delay_section()
        self._init_duration_section()
        # screenshots do not work on Wayland
        if not os.environ.get("WAYLAND_DISPLAY"):
            self._init_screenshot_section()
        return super().add_content()

    def _init_file_section(self):
        """Initializes UI elements for file and directory management."""
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        self.explorer_button = CustomPushButton(EXPLORER_DIALOG_TEXT)
        hbox.addWidget(self.explorer_button)
        self.dir_path_label = QLabel()
        hbox.addWidget(self.dir_path_label)
        vbox.addLayout(hbox)

        hbox = QHBoxLayout()
        fl = QLabel("Filename:")
        hbox.addWidget(fl)
        self.filename_textbox = QLineEdit()
        self.filename_textbox.setPlaceholderText("filename")
        hbox.addWidget(self.filename_textbox)
        vbox.addLayout(hbox)

        self.open_dir_button = CustomPushButton("Open directory")
        vbox.addWidget(self.open_dir_button)

        self._page_vbox.addLayout(vbox)

    def _init_enable_section(self):
        """Initializes the main record toggle button."""
        hbox = QHBoxLayout()

        self.record_toggle = CustomPushButton(RECORD_TOGGLE_OFF_TEXT)
        self.record_toggle.setCheckable(True)
        self.record_toggle.setEnabled(False)
        hbox.addWidget(self.record_toggle)

        self._page_vbox.addLayout(hbox)

    def _init_delay_section(self):
        """Initializes the slider for recording delay."""
        hbox = QHBoxLayout()

        hbox.addWidget(QLabel("Delay before recording"))

        self.recording_delay_slider = slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(120)
        slider.setValue(0)
        hbox.addWidget(slider)

        self.recording_delay_value_label = vl = QLabel(f"{slider.value()} s")
        hbox.addWidget(vl)

        self._page_vbox.addLayout(hbox)

    def _init_duration_section(self):
        """Initializes the UI for fixed-duration recordings."""
        vbox = QVBoxLayout()

        self.duration_checkbox = checkbox = QCheckBox("Limit recording duration")
        checkbox.setChecked(False)

        vbox.addWidget(checkbox)

        hbox = QHBoxLayout()
        self.duration_label = label = QLabel("Recording duration")
        label.setEnabled(False)
        hbox.addWidget(label)

        self.duration_slider = slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(3)
        slider.setMaximum(120)
        slider.setEnabled(False)
        slider.setValue(3)
        hbox.addWidget(slider)

        self.duration_descriptor = descriptor = QLabel(f"{slider.value()} s")
        descriptor.setEnabled(False)
        hbox.addWidget(descriptor)

        vbox.addLayout(hbox)

        self._page_vbox.addLayout(vbox)

    def _init_screenshot_section(self):
        """Initializes the screenshot checkbox (not available on Wayland)."""
        self.screenshot_checkbox = checkbox = QCheckBox(
            "Take screenshot when recording starts"
        )
        checkbox.setChecked(True)
        self._page_vbox.addWidget(checkbox)
