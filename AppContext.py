from typing import NamedTuple

from PyQt6.QtGui import QScreen

import screens
from Recorder import Recorder
from trackers.Tracker import Tracker
from trackers.Tracker import TrackerNotConnectedError
from trackers.tracker_selector import create_tracker
from visuals.visualizer.GazeVisualizer import GazeVisualizer


class OperationResult(NamedTuple):
    success: bool
    error: str | None = None


class AppContext:
    eyetracker: Tracker | None = None
    visualizer: GazeVisualizer
    recorder: Recorder = Recorder()
    screen: QScreen

    def __init__(self) -> None:
        self.screen = screens.get_primary_screen()
        self.visualizer = GazeVisualizer(screen=self.screen)
        pass

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
            self.screen = screen
        else:
            try:
                self.screen = screens.get_screen(screen)
            except screens.InvalidScreenBinding as e:
                self.screen = screens.get_primary_screen()
                return OperationResult(False, str(e))

        self.visualizer.bound_screen = self.screen
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
            screen_name = self.screen.name()
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
