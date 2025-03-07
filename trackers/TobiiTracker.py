import tobii_research as tr
import numpy as np
import atexit


class TobiiTracker:
    TOBII_LEFT = 'left_gaze_point_on_display_area'
    TOBII_RIGHT = 'right_gaze_point_on_display_area'

    def __init__(self):
        self.left_eye = None, None
        self.right_eye = None, None
        self.real_tracker = None
        self.__begin()
        atexit.register(self.__disable)

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

    def __gaze_callback(self, gaze_data):
        self.left_eye = gaze_data[TobiiTracker.TOBII_LEFT]
        self.right_eye = gaze_data[TobiiTracker.TOBII_RIGHT]

    def __disable(self):
        self.real_tracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA)  # type: ignore

    def sample(self):
        left_x, left_y = self.left_eye
        right_x, right_y = self.right_eye

        # Tobii marks closed eyes as NaNs
        left_open = left_x is not None and not np.isnan(left_x) and left_y is not None and not np.isnan(left_y)
        right_open = right_x is not None and not np.isnan(right_x) and right_y is not None and not np.isnan(right_y)

        if (left_open and right_open):
            assert left_x is not None and right_x is not None
            assert left_y is not None and right_y is not None
            return (((left_x + right_x) / 2), (left_y + right_y) / 2)
        elif left_open:
            return left_x, left_y
        elif right_open:
            return right_x, right_y
        else:
            return None, None
