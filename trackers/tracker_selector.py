from enum import Enum

from recording.Recorder import Recorder
from trackers.MouseTracker import MouseTracker
from trackers.TobiiTracker import TobiiTracker
from trackers.Tracker import Tracker
from visuals.visualizer.GazeVisualizer import GazeVisualizer


class TrackersEnum(Enum):
    DUMMY = 0
    TOBII = 1


DEFAULT: TrackersEnum = TrackersEnum.DUMMY


def create_tracker(
    tracker_type: TrackersEnum | str | None,
    visualizer: GazeVisualizer,
    recorder: Recorder,
) -> Tracker:
    if tracker_type is None:
        tracker_type = DEFAULT

    if isinstance(tracker_type, str):
        tracker_type = TrackersEnum[tracker_type.upper()]

    match tracker_type:
        case TrackersEnum.DUMMY:
            return MouseTracker(visualizer, recorder)
        case TrackersEnum.TOBII:
            return TobiiTracker(visualizer, recorder)
