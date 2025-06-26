import pytest

from processing.GazeStream import GazeStream
from trackers.GazePoint import GazePoint


def test_dispersion_simple():
    p1, p2 = GazePoint(0, 0, 0), GazePoint(10, 20, 0)
    stream = GazeStream()
    stream.append(p1)
    stream.append(p2)
    assert stream.dispersion() == pytest.approx(30)
