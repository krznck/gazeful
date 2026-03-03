"""Implementation of an eyetracker interface for Tobii hardware devices."""
import time

import numpy as np
import tobii_research as tr

from recording.Recorder import Recorder
from trackers.GazePoint import GazePoint
from trackers.Tracker import Tracker, TrackerNotConnectedError
from visuals.visualizer.GazeVisualizer import GazeVisualizer


class TobiiTracker(Tracker):
    """Hardware tracker implementation for Tobii eyetrackers.

    Attributes:
        TOBII_LEFT: Key for left eye data in Tobii SDK.
        TOBII_RIGHT: Key for right eye data in Tobii SDK.
        real_tracker: The underlying Tobii SDK tracker object.
    """

    TOBII_LEFT = "left_gaze_point_on_display_area"
    TOBII_RIGHT = "right_gaze_point_on_display_area"

    real_tracker = None

    def __init__(self, visualizer: GazeVisualizer, recorder: Recorder) -> None:
        """Initializes the Tobii tracker and starts data subscription.

        Args:
            visualizer: The visualizer that follows eye movement.
            recorder: The recorder that writes gaze data to a file.
        """
        super().__init__(visualizer, recorder)
        self._begin()

    def _begin(self):
        """Finds the connected Tobii tracker and subscribes to gaze data."""
        trackers = tr.find_all_eyetrackers()  # type: ignore
        if not trackers:
            raise TrackerNotConnectedError("The Tobii SDK could not find any tracker.")

        self.real_tracker = trackers[0]
        self.real_tracker.subscribe_to(
            tr.EYETRACKER_GAZE_DATA,  # type: ignore
            self._gaze_callback,
            as_dictionary=True,
        )

    def _gaze_callback(self, gaze_data) -> None:
        """Internal callback for Tobii gaze data events.

        Processes the dictionary from Tobii SDK, calculates averages for binocular
        tracking, and emits a GazePoint signal.

        Args:
            gaze_data: The dictionary containing gaze coordinates from the SDK.
        """
        if self.visualizer is None:
            return  # no need to do anything

        gaze = GazePoint(timestamp=time.monotonic())

        left_x, left_y = gaze_data[TobiiTracker.TOBII_LEFT]
        right_x, right_y = gaze_data[TobiiTracker.TOBII_RIGHT]

        left_open = coordinates_valid(left_x, left_y)
        right_open = coordinates_valid(right_x, right_y)

        if left_open and right_open:
            gaze.x = (left_x + right_x) / 2
            gaze.y = (left_y + right_y) / 2
        elif left_open:
            gaze.x, gaze.y = left_x, left_y
        elif right_open:
            gaze.x, gaze.y = right_x, right_y

        self.eyes_position_changed.emit(gaze)

    def stop(self) -> None:
        """Unsubscribes from the Tobii SDK and stops the tracking thread."""
        self.real_tracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA)  # type: ignore
        super().stop()

    @staticmethod
    def connected() -> bool:
        """Checks if any Tobii tracker is currently connected to the machine.

        Returns:
            True if one or more trackers are found.
        """
        return len(tr.find_all_eyetrackers()) > 0  # type: ignore


def coordinates_valid(cord1: float, cord2: float) -> bool:
    """Checks if a pair of coordinates are valid (not NaN).

    Args:
        cord1: The x-coordinate to check.
        cord2: The y-coordinate to check.

    Returns:
        True if neither coordinate is NaN.
    """
    return not np.isnan(cord1) and not np.isnan(cord2)
