from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox
from trackers.TrackerNotConnectedError import TrackerNotConnectedError
from trackers.fabricate_tracker import create_tracker
from visuals.GazeVisualizer import GazeVisualizer
from trackers.TrackersEnum import TrackersEnum
from trackers.Tracker import Tracker

_TITLE = "nnetp"


class MainWindow(QWidget):
    trackers_combo_box: QComboBox
    connect_button: QPushButton
    visualizer_toggle: QPushButton
    eyetracker: Tracker | None

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(_TITLE)

        window_vbox = QVBoxLayout()

        tracker_hbox = QHBoxLayout()

        self.trackers_combo_box = QComboBox()
        for tracker in TrackersEnum:
            self.trackers_combo_box.addItem(tracker.name.lower().capitalize())  # TOBII -> Tobii
        self.trackers_combo_box.currentIndexChanged.connect(self.on_combo_box_index_changed)
        tracker_hbox.addWidget(self.trackers_combo_box)

        self.connect_button = QPushButton("Not connected")
        self.connect_button.setCheckable(True)
        self.connect_button.clicked.connect(self.on_connection_button_clicked)
        tracker_hbox.addWidget(self.connect_button)

        window_vbox.addLayout(tracker_hbox)

        self.visualizer_toggle = QPushButton("Gaze visualizer: Off")
        self.visualizer_toggle.setCheckable(True)
        self.visualizer_toggle.clicked.connect(self.on_visualizer_toggle_clicked)
        self.visualizer_toggle.setDisabled(True)
        window_vbox.addWidget(self.visualizer_toggle)

        self.setLayout(window_vbox)

    def on_connection_button_clicked(self):
        if self.connect_button.isChecked():
            try:
                # 0 -> TrackersEnum.DUMMY -> MouseTracker object
                self.eyetracker = create_tracker(TrackersEnum(self.trackers_combo_box.currentIndex()))
                self.toggleConnectionButton(on=True)
            except TrackerNotConnectedError as e:
                self.toggleConnectionButton(on=False)
                QMessageBox.warning(self, "Connection problem", str(e))
        else:
            self.toggleVisualizerButton(on=False)
            self.toggleConnectionButton(on=False)
            if self.eyetracker:
                self.eyetracker.set_visualizer(None)
            self.eyetracker = None

    def on_visualizer_toggle_clicked(self):
        assert self.eyetracker
        self.toggleVisualizerButton(on=self.visualizer_toggle.isChecked())

    def on_combo_box_index_changed(self):
        self.toggleConnectionButton(on=False)
        if self.eyetracker:
            self.toggleVisualizerButton(on=False)
        self.eyetracker = None

    def toggleConnectionButton(self, on: bool):
        if on:
            self.connect_button.setText("Connected")
            self.connect_button.setChecked(True)
            self.visualizer_toggle.setEnabled(True)
        else:
            self.connect_button.setText("Not connected")
            self.connect_button.setChecked(False)
            self.visualizer_toggle.setDisabled(True)

    def toggleVisualizerButton(self, on: bool):
        assert self.eyetracker

        if on:
            self.eyetracker.set_visualizer(GazeVisualizer())
            self.eyetracker.start()
            self.visualizer_toggle.setChecked(True)
            self.visualizer_toggle.setText("Gaze visualizer: On")
        else:
            self.eyetracker.set_visualizer(None)
            self.eyetracker.quit()
            self.visualizer_toggle.setChecked(False)
            self.visualizer_toggle.setText("Gaze visualizer: Off")
