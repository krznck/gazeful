from pytest import approx
from pytest import raises

from processing.GazeStream import GazeStream
from processing.GazeStream import NonMonotonicTimesstampError
from trackers.GazePoint import GazePoint


def test_add_simple():
    gs = GazeStream()

    assert gs.is_empty()

    gs.add(GazePoint(0, 0, 0))

    assert not gs.is_empty()


def test_duration_simple():
    gs = GazeStream()

    # simulate four seconds of data
    gs.add(GazePoint(0, 0, 0))
    gs.add(GazePoint(0, 0, 1))
    gs.add(GazePoint(0, 0, 2))
    gs.add(GazePoint(0, 0, 3))
    gs.add(GazePoint(0, 0, 4))
    # there are five points of data, with first happening exactly at start of session,
    # and the last exactly at start of fourth second - so four seconds of data

    assert gs.get_duration() == approx(4)
    assert gs.length() == 5


def test_duration_non_monotone():
    gs = GazeStream()

    # simulate four seconds of data
    gs.add(GazePoint(0, 0, 0))
    gs.add(GazePoint(0, 0, 1))
    gs.add(GazePoint(0, 0, 2))
    gs.add(GazePoint(0, 0, 3))
    gs.add(GazePoint(0, 0, 4))

    with raises(NonMonotonicTimesstampError):
        gs.add(GazePoint(0, 0, 1.5))

    assert gs.length() == 5  # no alteration
