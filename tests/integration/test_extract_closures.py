from debug import ingest_sample
from processing.algorithms.ClosureAnalyzer import ClosureAnalyzer
from processing.Definitions import Definitions
from processing.GazeRecording import GazeRecording
from processing.GazeStream import GazeStream
from trackers.GazePoint import GazePoint

screen = (1920, 1200)


def test_two_closures():
    defs = Definitions()
    defs.blink_threshhold_ms.update(200)

    # here the closures are too long to be blinks
    pts = [
        GazePoint(0.1, 0.1, 0),
        GazePoint(0.1, 0.1, 0.1),
        GazePoint(0.1, 0.1, 0.4),
        GazePoint(None, None, 0.5),
        GazePoint(None, None, 1),
        GazePoint(0.5, 0.5, 1.2),
        GazePoint(0.5, 0.5, 1.5),
        GazePoint(0.5, 0.5, 2),
        GazePoint(None, None, 3),
        GazePoint(None, None, 5),
    ]

    recording = GazeRecording(data=GazeStream(pts), screen_dimensions=screen)
    analyzer = ClosureAnalyzer(recording, defs)
    closures = analyzer.extract_microsleeps()
    assert len(closures) == 2

    # here we reduce the time of the closures
    pts = [
        GazePoint(0.1, 0.1, 0),
        GazePoint(0.1, 0.1, 0.1),
        GazePoint(0.1, 0.1, 0.4),
        GazePoint(None, None, 0.5),
        GazePoint(None, None, 0.55),
        GazePoint(None, None, 0.60),
        GazePoint(0.5, 0.5, 1.2),
        GazePoint(0.5, 0.5, 1.5),
        GazePoint(0.5, 0.5, 2),
        GazePoint(None, None, 3),
        GazePoint(None, None, 3.15),
    ]

    recording = GazeRecording(data=GazeStream(pts), screen_dimensions=screen)
    analyzer = ClosureAnalyzer(recording, defs)
    closures = analyzer.extract_blinks()
    assert len(closures) == 2


def test_ars_technica_sample():
    defs = Definitions()
    defs.blink_threshhold_ms.update(400)

    recording = ingest_sample("ars_technica")
    assert not len(recording) == 0

    analyzer = ClosureAnalyzer(recording, defs)
    blinks = analyzer.extract_blinks()
    microsleeps = analyzer.extract_microsleeps()
    assert len(blinks) == 6
    assert len(microsleeps) == 3


def test_balatro_sample():
    defs = Definitions()
    defs.blink_threshhold_ms.update(400)

    recording = ingest_sample("balatro")
    assert not len(recording) == 0

    analyzer = ClosureAnalyzer(recording, defs)
    blinks = analyzer.extract_blinks()
    microsleeps = analyzer.extract_microsleeps()
    assert len(blinks) == 210
    assert len(microsleeps) == 120
