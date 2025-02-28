from trackers.MouseTracker import MouseTracker
from trackers.TobiiTracker import TobiiTracker
from trackers.TrackersEnum import TrackersEnum

DEFAULT: TrackersEnum = TrackersEnum.DUMMY


def create_tracker(tracker_type: TrackersEnum | str | None) -> MouseTracker | TobiiTracker:
    if tracker_type is None:
        tracker_type = DEFAULT

    if isinstance(tracker_type, str):
        tracker_type = TrackersEnum[tracker_type.upper()]

    match tracker_type:
        case TrackersEnum.DUMMY:
            return MouseTracker()
        case TrackersEnum.TOBII:
            return TobiiTracker()
