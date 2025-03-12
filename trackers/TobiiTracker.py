from visuals.GazeVisualizer import GazeVisualizer
from PyQt6.QtCore import QThread, pyqtSignal
import tobii_research as tr
import numpy as np
import atexit

class TobiiTracker(QThread):
    TOBII_LEFT = 'left_gaze_point_on_display_area'
    TOBII_RIGHT = 'right_gaze_point_on_display_area'

    gaze_sampled = pyqtSignal(float, float)
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

        # TODO: extract to clean this method up
        # Tobii marks closed eyes as NaNs
        left_open = (not np.isnan(left_x)
                     and
                     not np.isnan(left_y))
        right_open = (not np.isnan(right_x)
                      and
                      not np.isnan(right_y))

        if (left_open and right_open):
            self.gaze_sampled.emit(((left_x + right_x) / 2), (left_y + right_y) / 2)
        elif left_open:
            self.gaze_sampled.emit(left_x, left_y)
        elif right_open:
            self.gaze_sampled.emit(right_x, right_y)
        else:
            return  # TODO: Implement hiding visualizer
            # return None, None

    def __disable(self):
        self.real_tracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA)  # type: ignore

    # def sample(self):
    #     left_x, left_y = self.left_eye
    #     right_x, right_y = self.right_eye

    #     # Tobii marks closed eyes as NaNs
    #     left_open = left_x is not None and not np.isnan(left_x) and left_y is not None and not np.isnan(left_y)
    #     right_open = right_x is not None and not np.isnan(right_x) and right_y is not None and not np.isnan(right_y)

    #     if (left_open and right_open):
    #         assert left_x is not None and right_x is not None
    #         assert left_y is not None and right_y is not None
    #         return (((left_x + right_x) / 2), (left_y + right_y) / 2)
    #     elif left_open:
    #         return left_x, left_y
    #     elif right_open:
    #         return right_x, right_y
    #     else:
    #         return None, None
