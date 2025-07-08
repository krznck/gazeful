from pathlib import Path
from typing import NamedTuple

from PyQt6.QtGui import QScreen

import screens
from processing.Definitions import Definitions
from processing.GazeRecording import GazeRecording
from processing.GazeStream import GazeStream
from processing.ingester import ingest_csv
from recording.Recorder import Recorder
from trackers.Tracker import Tracker
from trackers.Tracker import TrackerNotConnectedError
from trackers.tracker_selector import create_tracker
from trackers.tracker_selector import default_to_first_connected
from visuals.visualizer.GazeVisualizer import GazeVisualizer


class OperationResult(NamedTuple):
    success: bool
    error: str | None = None


class AppContext:
    def __init__(self) -> None:
        self.tracked_screen: QScreen = screens.get_primary_screen()
        self.recorder: Recorder = Recorder(screens.get_screen_size(self.tracked_screen))
        self.defs: Definitions = Definitions()
        self.visualizer: GazeVisualizer = GazeVisualizer(screen=self.tracked_screen)
        self.eyetracker: Tracker | None = default_to_first_connected(
            self.visualizer, self.recorder
        )
        self.eyetracker.track()
        self._main_data: GazeRecording | None = None

    @property
    def main_data(self) -> GazeRecording | None:
        return self._main_data

    @main_data.setter
    def main_data(self, data: GazeStream | Path):
        if isinstance(data, GazeStream):
            self._main_data = GazeRecording(data)
        elif isinstance(data, Path):
            self._main_data = ingest_csv(data)

    def connect_tracker(self, tracker: str) -> OperationResult:
        try:
            self.eyetracker = create_tracker(tracker, self.visualizer, self.recorder)
        except TrackerNotConnectedError as e:
            self.disconnect_tracker()
            return OperationResult(False, str(e))

        self.eyetracker.track()
        return OperationResult(True)

    def disconnect_tracker(self):
        if self.eyetracker is not None:
            self.eyetracker.stop()
        self.eyetracker = None

    def specify_screen(self, screen: str | QScreen) -> OperationResult:
        if isinstance(screen, QScreen):
            self.tracked_screen = screen
        else:
            try:
                self.tracked_screen = screens.get_screen(screen)
            except screens.InvalidScreenBinding as e:
                self.tracked_screen = screens.get_primary_screen()
                return OperationResult(False, str(e))

        self.visualizer.bound_screen = self.tracked_screen
        self.recorder.set_screen(screens.get_screen_size(self.tracked_screen))
        return OperationResult(True)

    def check_screens_state(self) -> tuple[OperationResult, list[str], int]:
        """Checks whether the currently chosen screen is still connected to the machine.
        If not, defaults to the primary screen.
        Returns:
            ConnectResult: positive when it is, otherwise negative with warning
            list[str]: names of all screens accessible to the application
            int: index on that list of the chosen screen after the check
        """
        names = screens.get_screen_names()
        primary = screens.get_primary_screen()
        primary_index = None

        try:
            screen_name = self.tracked_screen.name()
        except RuntimeError:
            # "wrapped C/C++ object of type QScreen has been deleted" -> check negative
            screen_name = None

        for index, name in enumerate(names):
            if screen_name == name:
                return OperationResult(True), names, index

            if primary.name() == name:
                primary_index = index

        assert primary_index is not None  # if primary not in list, assumptions are bad

        self.specify_screen(primary)
        warning = (
            "Previously chosen screen is no longer accessible. "
            + "Defaulting to primary screen."
        )
        return OperationResult(False, warning), names, primary_index

    def toggle_visualizer(self, on: bool | None = None) -> None:
        if isinstance(on, bool):
            self.visualizer.toggle(on)
        else:
            self.visualizer.toggle(not self.visualizer.enabled)
