import time

import numpy as np
import tobii_research as tr

from trackers.GazePoint import GazePoint
from trackers.Tracker import Tracker
from trackers.Tracker import TrackerNotConnectedError
from visuals.visualizer.GazeVisualizer import GazeVisualizer


class TobiiTracker(Tracker):
    TOBII_LEFT = "left_gaze_point_on_display_area"
    TOBII_RIGHT = "right_gaze_point_on_display_area"

    real_tracker = None

    def __init__(self, visualizer: GazeVisualizer | None = None) -> None:
        super().__init__(visualizer)
        self.__begin()

    def __begin(self):
        trackers = tr.find_all_eyetrackers()  # type: ignore
        if not trackers:
            raise TrackerNotConnectedError("The Tobii SDK could not find any tracker.")

        self.real_tracker = trackers[0]
        self.real_tracker.subscribe_to(
            tr.EYETRACKER_GAZE_DATA,  # type: ignore
            self.__gaze_callback,
            as_dictionary=True,
        )

    def __gaze_callback(self, gaze_data) -> None:
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
        self.real_tracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA)  # type: ignore
        super().stop()


def coordinates_valid(cord1: float, cord2: float) -> bool:
    return not np.isnan(cord1) and not np.isnan(cord2)
