"""The home page of the application, used for tracker and screen selection."""
import os

import screens
from PyQt6.QtWidgets import QComboBox, QHBoxLayout, QPushButton
from trackers.tracker_selector import TrackersEnum

from visuals.assets.icon_selector import IconsEnum
from visuals.customized_widgets.CustomComboBox import CustomComboBox
from visuals.customized_widgets.CustomPushButton import CustomPushButton
from visuals.pages.Page import Page


class MainPage(Page):
    """The home page for configuring hardware and monitoring settings.

    Attributes:
        trackers_combo_box: Dropdown for selecting the eyetracker.
        screens_combo_box: Dropdown for selecting the screen to track.
        connect_toggle: Button to connect/disconnect the tracker.
        visualizer_toggle: Button to show/hide the gaze visualizer.
    """

    trackers_combo_box: QComboBox
    screens_combo_box: QComboBox
    connect_toggle: QPushButton
    visualizer_toggle: QPushButton | None

    _screens_refreshing = False

    def __init__(self) -> None:
        """Initializes the main page."""
        self.visualizer_toggle = None
        super().__init__("Home", IconsEnum.HOME)

    def add_content(self) -> None:
        """Adds page content, including tracker, screen, and visualizer sections."""
        self._init_tracker_section()
        self._init_screens_section()
        if not os.environ.get("WAYLAND_DISPLAY"):
            self._init_visualizer_section()

    def _init_tracker_section(self):
        """Initializes the section for selecting and connecting a tracker."""
        hbox = QHBoxLayout()

        tcb = self.trackers_combo_box = CustomComboBox()
        for tracker in TrackersEnum:
            self.trackers_combo_box.addItem(tracker.name.lower().capitalize())
        hbox.addWidget(tcb)

        ct = self.connect_toggle = CustomPushButton("Connected")
        ct.setMinimumWidth(100)  # should be same size when on and off
        ct.setCheckable(True)
        ct.setChecked(True)
        hbox.addWidget(ct)

        self._page_vbox.addLayout(hbox)

    def _init_screens_section(self):
        """Initializes the section for selecting and refreshing connected screens."""
        hbox = QHBoxLayout()

        self.screens_combo_box = CustomComboBox()
        for index, name in enumerate(screens.get_screen_names()):
            self.screens_combo_box.addItem(str(index + 1) + ": " + name)
        hbox.addWidget(self.screens_combo_box)

        self.screen_refresh_button = CustomPushButton("Refresh")
        hbox.addWidget(self.screen_refresh_button)

        self._page_vbox.addLayout(hbox)

    def _init_visualizer_section(self):
        """Initializes the visualizer toggle button (not available on Wayland)."""
        hbox = QHBoxLayout()

        self.visualizer_toggle = CustomPushButton("Gaze visualizer: Off")
        self.visualizer_toggle.setCheckable(True)
        hbox.addWidget(self.visualizer_toggle)

        self._page_vbox.addLayout(hbox)
