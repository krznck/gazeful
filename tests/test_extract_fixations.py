"""Integration tests for fixation extraction using oculomotor analyzers."""
import pytest
from debug import Samples, debug_time, ingest_sample
from processing.algorithms.OculomotorAnalyzer import OculomotorAnalyzer
from processing.GazeRecording import GazeRecording
from processing.GazeStream import GazeStream
from pytest import approx
from trackers.GazePoint import GazePoint

screen = (1920, 1200)


def test_two_fixations():
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

    recording = GazeRecording(data=GazeStream(pts), screen_dimensions=screen)
    analyzer = OculomotorAnalyzer(recording, 200, 65)
    fixations = analyzer.extract_fixations()

    assert len(fixations) == 2


def test_dispersion_breakup():
    # even a tiny dispersion should break the fixation
    duration = 100
    disp = 0.00001

    pts = [
        GazePoint(0.1, 0.1, 0),
        GazePoint(0.1, 0.1, 1.2),  # <- should be 1st fixation of 1.2 seconds
    ]

    recording = GazeRecording(data=GazeStream(pts), screen_dimensions=screen)
    analyzer = OculomotorAnalyzer(recording, duration, disp)
    fixations = analyzer.extract_fixations()
    assert len(fixations) == 1

    stream = recording.data
    stream.append(GazePoint(0.2, 0.2, 1.3))
    stream.append(GazePoint(0.2, 0.2, 1.5))  # <- should count new fix due to dispersion
    analyzer = OculomotorAnalyzer(recording, duration, disp)
    fixations = analyzer.extract_fixations()
    assert len(fixations) == 2

    # too far from previous fixation, but didn't take up enough time -> should not count
    stream.append(GazePoint(0.9, 0.9, 1.6))
    analyzer = OculomotorAnalyzer(recording, duration, disp)
    fixations = analyzer.extract_fixations()
    assert len(fixations) == 2


def prepare_sample(sample: str) -> OculomotorAnalyzer:
    """Helper to ingest a sample CSV and wrap it in an analyzer.

    Args:
        sample: Name of the sample file.

    Returns:
        An OculomotorAnalyzer initialized with default thresholds.
    """
    recording = ingest_sample(sample)
    assert not len(recording) == 0

    return OculomotorAnalyzer(recording, 200, 65)


def test_one_fixation_sample():
    analyzer = prepare_sample(Samples.ONE.value)
    fixations = analyzer.extract_fixations()
    assert len(fixations) == 1


# sample of a gaze session of reading an article from Ars Technica
def test_ars_technica_sample():
    analyzer = prepare_sample(Samples.ARS.value)
    fixations = analyzer.extract_fixations()
    assert len(fixations) == 417
    assert round(analyzer.average_fixation_duration(), 2) == approx(306.45)
    assert analyzer.median_fixation_duration() == approx(281)


# sample of a gaze session of playing Balatro
def test_balatro_sample():
    analyzer = prepare_sample(Samples.BALATRO.value)
    fixations = analyzer.extract_fixations()
    assert len(fixations) == 1483
    assert round(analyzer.average_fixation_duration(), 2) == approx(284.26)
    assert analyzer.median_fixation_duration() == approx(250)


@pytest.mark.perf
def test_perfomace():
    for sample in Samples:
        debug_time(
            func=lambda: prepare_sample(sample.value).extract_fixations(),
            message=f"{sample.value} fixation extraction",
        )
