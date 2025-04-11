from PyQt6.QtCore import Qt
from PyQt6.QtGui import QScreen
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget

import screens
from trackers.Tracker import Tracker
from trackers.Tracker import TrackerNotConnectedError
from trackers.tracker_selector import create_tracker
from trackers.tracker_selector import TrackersEnum
from visuals.customized_widgets.CustomComboBox import CustomComboBox
from visuals.customized_widgets.CustomPushButton import CustomPushButton
from visuals.visualizer.GazeVisualizer import GazeVisualizer

_TITLE = "nnetp"
_CONNECTION_BUTTON_CONNECTED_TEXT: str = "Connected"
_CONNECTION_BUTTON_DISCONNECTED_TEXT: str = "Disconnected"
_VISUALIZER_BUTTON_ON_TEXT: str = "Gaze visualizer: On"
_VISUALIZER_BUTTON_OFF_TEXT: str = "Gaze visualizer: Off"
_VIS_ANIMATIONS_BUTTON_ON_TEXT: str = "Animations: On"
_VIS_ANIMATIONS_BUTTON_OFF_TEXT: str = "Animations: Off"


class MainWindow(QWidget):
    trackers_combo_box: QComboBox
    connect_button: QPushButton
    screens_combo_box: QComboBox
    screen_refresh_button: QPushButton
    visualizer_toggle: QPushButton

    eyetracker: Tracker | None
    tracking_screen: QScreen

    __screens_refreshing = False

    def __init__(self) -> None:
        super().__init__()

        # we'll choose the primary as the default
        self.tracking_screen = screens.get_primary_screen()

        self.eyetracker = None
        self.setWindowTitle(_TITLE)

        window_vbox = QVBoxLayout()

        tracker_hbox = QHBoxLayout()

        self.trackers_combo_box = CustomComboBox()
        for tracker in TrackersEnum:
            # TOBII -> Tobii
            self.trackers_combo_box.addItem(tracker.name.lower().capitalize())

        self.trackers_combo_box.currentIndexChanged.connect(
            self.on_trackers_combo_box_index_changed
        )
        tracker_hbox.addWidget(self.trackers_combo_box)

        self.connect_button = CustomPushButton(_CONNECTION_BUTTON_DISCONNECTED_TEXT)
        self.connect_button.setMinimumWidth(
            100
        )  # we want it to stay the same size regardless of text
        self.connect_button.setCheckable(True)

        self.connect_button.clicked.connect(self.on_connection_button_clicked)

        tracker_hbox.addWidget(self.connect_button)

        window_vbox.addLayout(tracker_hbox)

        screens_hbox = QHBoxLayout()
        self.screens_combo_box = CustomComboBox()
        for index, name in enumerate(screens.get_screen_names()):
            self.screens_combo_box.addItem(str(index + 1) + ": " + name)
        self.screens_combo_box.currentIndexChanged.connect(
            self.on_screens_combo_box_index_changed
        )
        screens_hbox.addWidget(self.screens_combo_box)

        self.screen_refresh_button = CustomPushButton("Refresh")
        self.screen_refresh_button.clicked.connect(
            self.on_screen_refresh_button_clicked
        )
        screens_hbox.addWidget(self.screen_refresh_button)

        window_vbox.addLayout(screens_hbox)

        visualizer_hbox = QHBoxLayout()

        self.visualizer_toggle = CustomPushButton(_VISUALIZER_BUTTON_OFF_TEXT)
        self.visualizer_toggle.setCheckable(True)
        self.visualizer_toggle.clicked.connect(self.on_visualizer_toggle_clicked)
        self.visualizer_toggle.setDisabled(True)
        visualizer_hbox.addWidget(self.visualizer_toggle)

        self.vis_animation_toggle = CustomPushButton(_VIS_ANIMATIONS_BUTTON_ON_TEXT)
        self.vis_animation_toggle.setCheckable(True)
        self.vis_animation_toggle.setChecked(True)
        self.vis_animation_toggle.clicked.connect(self.on_vis_animation_button_toggle)
        visualizer_hbox.addWidget(self.vis_animation_toggle)

        window_vbox.addLayout(visualizer_hbox)

        window_vbox.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(window_vbox)

    def closeEvent(self, a0) -> None:
        if self.eyetracker is not None:
            self.eyetracker.stop()
        return super().closeEvent(a0)

    def on_connection_button_clicked(self):
        if self.connect_button.isChecked():
            try:
                # 0 -> TrackersEnum.DUMMY -> MouseTracker object
                self.eyetracker = create_tracker(
                    TrackersEnum(self.trackers_combo_box.currentIndex())
                )
                self.toggleConnectionButton(on=True)
            except TrackerNotConnectedError as e:
                self.toggleConnectionButton(on=False)
                QMessageBox.warning(self, _CONNECTION_BUTTON_DISCONNECTED_TEXT, str(e))
        else:
            self.toggleVisualizerButton(on=False)
            self.toggleConnectionButton(on=False)
            if self.eyetracker:
                self.eyetracker.set_visualizer(None)
            self.eyetracker = None

    def on_visualizer_toggle_clicked(self):
        assert self.eyetracker
        self.toggleVisualizerButton(on=self.visualizer_toggle.isChecked())

    def on_screen_refresh_button_clicked(self):
        self.__screens_refreshing = True
        screen_matched = (
            False  # after refresh, possible that the chosen screen is no longer here
        )

        default_screen = screens.get_primary_screen()
        default_index = None
        try:
            self.screens_combo_box.clear()
            screen_names = screens.get_screen_names()
            for index, name in enumerate(screen_names):
                self.screens_combo_box.addItem(str(index + 1) + ": " + name)
                if name == default_screen.name():
                    default_index = index
                if name == self.tracking_screen.name():
                    screen_matched = True
                    self.tracking_screen = screens.get_screen(index)
                    self.screens_combo_box.setCurrentIndex(index)
        except RuntimeError:
            # "wrapped C/C++ object of type QScreen has been deleted" -> naturally means the screen is not accessible
            screen_matched = False

        # if the primary screen wasn't on the list, assumptions on how this works are wrong
        assert default_index is not None

        if not screen_matched:
            _ = QMessageBox.warning(
                self,
                "Screen configuration warning",
                "The previously chosen screen is no longer accessible. "
                + "Defaulting to the current primary screen.",
            )
            self.tracking_screen = default_screen
            self.screens_combo_box.setCurrentIndex(default_index)

        self.__screens_refreshing = False

    def on_trackers_combo_box_index_changed(self):
        self.toggleConnectionButton(on=False)
        if self.eyetracker:
            self.toggleVisualizerButton(on=False)
        self.eyetracker = None

    def on_screens_combo_box_index_changed(self):
        if self.__screens_refreshing:
            return

        try:
            self.tracking_screen = screens.get_screen(
                self.screens_combo_box.currentText().split(": ", 1)[-1]
            )
        except screens.InvalidScreenBinding as e:
            QMessageBox.warning(
                self, "Screen warning", (str(e) + " Refreshing the list.")
            )
            self.tracking_screen = screens.get_primary_screen()
            self.screen_refresh_button.click()

        if self.eyetracker is not None and self.eyetracker.visualizer is not None:
            self.eyetracker.visualizer.bound_screen = self.tracking_screen

    def on_vis_animation_button_toggle(self):
        if self.eyetracker is not None and self.eyetracker.visualizer is not None:
            self.eyetracker.visualizer.animations = (
                self.vis_animation_toggle.isChecked()
            )

        self.vis_animation_toggle.setText(
            _VIS_ANIMATIONS_BUTTON_ON_TEXT
            if self.vis_animation_toggle.isChecked()
            else _VIS_ANIMATIONS_BUTTON_OFF_TEXT
        )

    def toggleConnectionButton(self, on: bool):
        if on:
            self.connect_button.setText(_CONNECTION_BUTTON_CONNECTED_TEXT)
            self.connect_button.setChecked(True)
            self.visualizer_toggle.setEnabled(True)
        else:
            self.connect_button.setText(_CONNECTION_BUTTON_DISCONNECTED_TEXT)
            self.connect_button.setChecked(False)
            self.visualizer_toggle.setDisabled(True)

    def toggleVisualizerButton(self, on: bool):
        assert self.eyetracker

        if on:
            self.eyetracker.set_visualizer(
                GazeVisualizer(
                    screen=self.tracking_screen,
                    animations=self.vis_animation_toggle.isChecked(),
                )
            )
            self.eyetracker.start()
            self.visualizer_toggle.setChecked(True)
            self.visualizer_toggle.setText(_VISUALIZER_BUTTON_ON_TEXT)
        else:
            self.eyetracker.set_visualizer(None)
            self.eyetracker.quit()
            self.visualizer_toggle.setChecked(False)
            self.visualizer_toggle.setText(_VISUALIZER_BUTTON_OFF_TEXT)
