from pytest import approx

from debug import debug_time
from debug import ingest_sample
from processing.algorithms.OculomotorAnalyzer import OculomotorAnalyzer
from processing.Definitions import Definitions
from processing.GazeStream import GazeStream
from trackers.GazePoint import GazePoint


def test_two_fixations():
    defs = Definitions()
    defs.blink_threshhold_ms.update(200)  # a blink is minimum 200ms
    defs.fixation_minimum_duration_ms.update(200)  # a fixation as well

    pts = [
        GazePoint(0.1, 0.1, 0),
        GazePoint(0.1, 0.1, 0.1),
        GazePoint(0.1, 0.1, 0.4),
        GazePoint(None, None, 0.5),
        GazePoint(None, None, 1),
        GazePoint(0.5, 0.5, 1.2),
        GazePoint(0.5, 0.5, 1.5),
        GazePoint(0.5, 0.5, 2),
    ]

    stream = GazeStream(pts)
    analyzer = OculomotorAnalyzer(stream, defs)
    fixations = analyzer.extract_fixations()

    assert len(fixations) == 2


def test_dispersion_breakup():
    defs = Definitions()
    # even a tiny dispersion should break the fixation
    defs.fixation_maximum_dispersion_screen_area_percent.update(0.00001)
    defs.fixation_minimum_duration_ms.update(100)

    pts = [
        GazePoint(0.1, 0.1, 0),
        GazePoint(0.1, 0.1, 1.2),  # <- should be 1st fixation of 1.2 seconds
    ]

    stream = GazeStream(pts)
    analyzer = OculomotorAnalyzer(stream, defs)
    fixations = analyzer.extract_fixations()
    assert len(fixations) == 1

    stream.append(GazePoint(0.2, 0.2, 1.3))
    stream.append(GazePoint(0.2, 0.2, 1.5))  # <- should count new fix due to dispersion
    analyzer = OculomotorAnalyzer(stream, defs)
    fixations = analyzer.extract_fixations()
    assert len(fixations) == 2

    # too far from previous fixation, but didn't take up enough time -> should not count
    stream.append(GazePoint(0.9, 0.9, 1.6))
    analyzer = OculomotorAnalyzer(stream, defs)
    fixations = analyzer.extract_fixations()
    assert len(fixations) == 2


def test_one_fixation_sample():
    print("\n-- One fixation --\n")
    defs = Definitions()
    defs.fixation_maximum_dispersion_screen_area_percent.update(0.05)
    defs.fixation_minimum_duration_ms.update(200)

    points = debug_time(lambda: ingest_sample("one_fix"))
    stream = GazeStream(points)
    assert not stream.is_empty()

    analyzer = OculomotorAnalyzer(stream, defs)
    fixations = analyzer.extract_fixations()
    assert len(fixations) == 1


# sample of a gaze session of reading an article from Ars Technica
def test_ars_technica_sample():
    print("\n-- Ars Technica --\n")
    defs = Definitions()
    defs.fixation_maximum_dispersion_screen_area_percent.update(0.05)
    defs.fixation_minimum_duration_ms.update(200)

    points = debug_time(lambda: ingest_sample("ars_technica"))
    stream = debug_time(lambda: GazeStream(points))
    # stream = GazeStream(points)
    assert not stream.is_empty()

    analyzer = OculomotorAnalyzer(stream, defs)
    fixations = analyzer.extract_fixations()
    assert len(fixations) == 379
    assert round(analyzer.average_fixation_duration(), 2) == approx(359.67)
    assert analyzer.median_fixation_duration() == approx(313)


# sample of a gaze session of playing Balatro
def test_balatro_sample():
    print("\n-- Balatro --\n")
    defs = Definitions()
    defs.fixation_maximum_dispersion_screen_area_percent.update(0.05)
    defs.fixation_minimum_duration_ms.update(200)

    points = debug_time(lambda: ingest_sample("balatro"))
    stream = debug_time(lambda: GazeStream(points))
    # stream = GazeStream(points)
    assert not stream.is_empty()

    analyzer = OculomotorAnalyzer(stream, defs)
    fixations = analyzer.extract_fixations()
    assert len(fixations) == 1457
    assert round(analyzer.average_fixation_duration(), 2) == approx(288.95)
    assert analyzer.median_fixation_duration() == approx(250)
