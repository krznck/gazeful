from trackers.fabricate_tracker import create_tracker
from trackers.TrackersEnum import TrackersEnum
from visuals.GazeVisualizer import GazeVisualizer
from PyQt6.QtWidgets import QApplication
import sys


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
    app = QApplication([])
    window = GazeVisualizer()
    tracker = create_tracker(parse_arguments())
    tracker.set_visualizer(window)
    tracker.start()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
