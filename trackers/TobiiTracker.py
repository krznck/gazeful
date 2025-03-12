from visuals.GazeVisualizer import GazeVisualizer
from PyQt6.QtCore import QThread, pyqtSignal
import tobii_research as tr
import numpy as np
import atexit


class TobiiTracker(QThread):
    TOBII_LEFT = 'left_gaze_point_on_display_area'
    TOBII_RIGHT = 'right_gaze_point_on_display_area'

    gaze_sampled = pyqtSignal(object, object)  # in our case, should be a tuple of floats or Nones
    visualizer: GazeVisualizer
    real_tracker = None

    def __init__(self, visualizer: GazeVisualizer | None = None) -> None:
        super().__init__()
        self.__begin()
        atexit.register(self.__disable)

        if (visualizer is not None):
            self.set_visualizer(visualizer)

    def set_visualizer(self, visualizer: GazeVisualizer) -> None:
        self.visualizer = visualizer
        self.gaze_sampled.connect(visualizer.set_position)

    def __begin(self):
        trackers = tr.find_all_eyetrackers()  # type: ignore
        # TODO: change to an exception
        if not trackers:
            print("Did not find any Tobii trackers connected to the computer.")
            exit(1)

        self.real_tracker = trackers[0]
        self.real_tracker.subscribe_to(
            tr.EYETRACKER_GAZE_DATA,  # type: ignore
            self.__gaze_callback,
            as_dictionary=True)

    def __gaze_callback(self, gaze_data) -> None:
        if (self.visualizer is None):
            return  # no need to do anything

        left_x, left_y = gaze_data[TobiiTracker.TOBII_LEFT]
        right_x, right_y = gaze_data[TobiiTracker.TOBII_RIGHT]

        left_open = coordinates_valid(left_x, left_y)
        right_open = coordinates_valid(right_x, right_y)

        if (left_open and right_open):
            self.gaze_sampled.emit(((left_x + right_x) / 2), (left_y + right_y) / 2)
        elif left_open:
            self.gaze_sampled.emit(left_x, left_y)
        elif right_open:
            self.gaze_sampled.emit(right_x, right_y)
        else:
            # return  # TODO: Implement hiding visualizer
            self.gaze_sampled.emit(None, None)

    def __disable(self):
        self.real_tracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA)  # type: ignore


def coordinates_valid(cord1: float, cord2: float) -> bool:
    return not np.isnan(cord1) and not np.isnan(cord2)
