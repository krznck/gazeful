from trackers.fabricate_tracker import create_tracker
from trackers.TrackersEnum import TrackersEnum
import visualize_gaze as vg
import threading
import time
import sys

LIFETIME: int = 5000


def track(tracker, window, event: threading.Event):
    time.sleep(1)
    while not event.is_set():
        x, y = tracker.sample()
        vg.update_position(x, y, window)


def stop_tracking(window, event: threading.Event):
    event.set()
    window.destroy()


def parse_arguments() -> str | None:
    args = sys.argv[1:]  # we don't care about 0th argument here (program path)
    allowed_values = TrackersEnum.__members__.keys()

    match len(args):
        case 0:
            return None
        case 1 if args[0] in allowed_values:
            return args[0]
        case _:
            print(f"Allowed arguments: {', '.join(allowed_values)}")
            exit(1)


def main():
    window = vg.draw_visualizer()
    stop_event = threading.Event()

    tracking_args = (create_tracker(parse_arguments()), window, stop_event)
    track_thread = threading.Thread(target=track, args=(tracking_args), daemon=True)
    track_thread.start()

    window.after(LIFETIME, lambda: stop_tracking(window, stop_event))
    window.mainloop()


main()
