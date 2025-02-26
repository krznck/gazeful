import threading
from trackers.MouseTracker import MouseTracker
from trackers.TobiiTracker import TobiiTracker
from trackers.TrackersEnum import TrackersEnum
import visualize_gaze as vg
import time

CHOSEN_TRACKER: TrackersEnum = TrackersEnum.DUMMY
LIFETIME: int = 5000


def track(tracker, window, event: threading.Event):
    time.sleep(1)
    while not event.is_set():
        x, y = tracker.sample()
        vg.update_position(x, y, window)


def stop_tracking(window, event: threading.Event):
    event.set()
    window.destroy()


def create_tracker(tracker_type: TrackersEnum):
    match tracker_type:
        case TrackersEnum.DUMMY:
            return MouseTracker()
        case TrackersEnum.TOBII:
            return TobiiTracker()


def main():
    window = vg.draw_visualizer()
    stop_event = threading.Event()

    args = (create_tracker(CHOSEN_TRACKER), window, stop_event)
    track_thread = threading.Thread(target=track, args=(args), daemon=True)
    track_thread.start()

    window.after(LIFETIME, lambda: stop_tracking(window, stop_event))
    window.mainloop()


main()
