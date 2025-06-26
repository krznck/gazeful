from pytest import approx
from pytest import raises

from processing.GazeStream import GazeStream
from processing.GazeStream import NonMonotonicTimesstampError
from trackers.GazePoint import GazePoint


def test_add_simple():
    gs = GazeStream()

    assert gs.is_empty()

    gs.append(GazePoint(0, 0, 0))

    assert not gs.is_empty()


def test_duration_simple():
    gs = GazeStream()

    # simulate four seconds of data
    gs.append(GazePoint(0, 0, 0))
    gs.append(GazePoint(0, 0, 1))
    gs.append(GazePoint(0, 0, 2))
    gs.append(GazePoint(0, 0, 3))
    gs.append(GazePoint(0, 0, 4))
    # there are five points of data, with first happening exactly at start of session,
    # and the last exactly at start of fourth second - so four seconds of data

    assert gs.duration() == approx(4)
    assert len(gs) == 5


def test_duration_non_monotone():
    gs = GazeStream()

    # simulate four seconds of data
    gs.append(GazePoint(0, 0, 0))
    gs.append(GazePoint(0, 0, 1))
    gs.append(GazePoint(0, 0, 2))
    gs.append(GazePoint(0, 0, 3))
    gs.append(GazePoint(0, 0, 4))

    with raises(NonMonotonicTimesstampError):
        gs.append(GazePoint(0, 0, 1.5))

    assert len(gs) == 5  # no alteration


def test_centroid_simple():
    gs = GazeStream()

    gs.append(GazePoint(0, 0, 1))
    gs.append(GazePoint(1, 1, 2))

    assert gs.centroid() == (0.5, 0.5)
