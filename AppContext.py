"""Global application state and service container."""
from pathlib import Path
from typing import NamedTuple

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QScreen

import screens
from processing.GazeRecording import GazeRecording
from processing.GazeStream import GazeStream
from processing.ingester import ingest_csv
from recording.Recorder import Recorder
from trackers.Tracker import Tracker, TrackerNotConnectedError
from trackers.tracker_selector import (create_tracker,
                                       default_to_first_connected)
from visuals.visualizer.GazeVisualizer import GazeVisualizer


class OperationResult(NamedTuple):
    """Result of a state-changing operation.

    Attributes:
        success: Whether the operation completed successfully.
        error: An error message if success is False.
    """
    success: bool
    error: str | None = None


class AppContext(QObject):
    """Central container for application-wide state and shared services.

    Manages hardware connections, screen tracking, and the global data recording.

    Attributes:
        main_data_changed: Signal emitted whenever the primary gaze recording is updated.
        tracked_screen: The monitor currently selected for tracking.
        recorder: The service handling data persistence.
        visualizer: The overlay for real-time gaze visualization.
        eyetracker: The currently active tracker hardware or simulation.
    """
    main_data_changed = pyqtSignal()

    def __init__(self) -> None:
        """Initializes the application context and hardware connections."""
        super().__init__()
        self.tracked_screen: QScreen = screens.get_primary_screen()
        self.recorder: Recorder = Recorder(screens.get_screen_size(self.tracked_screen))
        self.visualizer: GazeVisualizer = GazeVisualizer(screen=self.tracked_screen)
        self.eyetracker: Tracker | None = default_to_first_connected(
            self.visualizer, self.recorder
        )
        self.eyetracker.track()
        self._main_data: GazeRecording | None = None

    @property
    def main_data(self) -> GazeRecording | None:
        """The currently active gaze recording."""
        return self._main_data

    @main_data.setter
    def main_data(self, data: GazeStream | Path | GazeRecording):
        """Sets the active gaze data, accepting a stream, a path, or a recording object.

        Args:
            data: The new gaze data to load into the context.
        """
        match data:
            case Path() as path:
                self._main_data = ingest_csv(path)
            case GazeStream() as stream:
                self._main_data = GazeRecording(
                    data=stream,
                    screen_dimensions=screens.get_screen_size(self.tracked_screen),
                )
            case GazeRecording() as recording:
                self._main_data = recording

        self.main_data_changed.emit()

    def connect_tracker(self, tracker: str) -> OperationResult:
        """Attempts to connect to a specific tracker hardware.

        Args:
            tracker: The name of the tracker to connect to.

        Returns:
            OperationResult indicating success or failure.
        """
        try:
            self.eyetracker = create_tracker(tracker, self.visualizer, self.recorder)
        except TrackerNotConnectedError as e:
            self.disconnect_tracker()
            return OperationResult(False, str(e))

        self.eyetracker.track()
        return OperationResult(True)

    def disconnect_tracker(self):
        """Stops and disconnects the current tracker."""
        if self.eyetracker is not None:
            self.eyetracker.stop()
        self.eyetracker = None

    def specify_screen(self, screen: str | QScreen) -> OperationResult:
        """Binds the application to a specific screen for tracking.

        Args:
            screen: The name of the screen or a QScreen object.

        Returns:
            OperationResult indicating if the binding was successful.
        """
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
            A tuple containing:
                - OperationResult: positive when it is, otherwise negative with warning
                - list[str]: names of all screens accessible to the application
                - int: index on that list of the chosen screen after the check
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
        """Toggles the gaze visualizer overlay.

        Args:
            on: Explicit state to set. If None, toggles current state.
        """
        if on is not None:
            self.visualizer.toggle(on)
        else:
            self.visualizer.toggle(not self.visualizer.enabled)
