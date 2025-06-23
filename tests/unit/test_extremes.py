import pytest

from processing.algorithms.OculomotorAnalyzer import Extremes
from processing.GazeStream import GazeStream
from trackers.GazePoint import GazePoint


def test_dispersion_simlple():
    p1, p2 = GazePoint(0, 0, 0), GazePoint(10, 20, 0)
    extremes = Extremes(max_x=p1, max_y=p1, min_x=p1, min_y=p1)
    extremes.update(p2)
    assert extremes.dispersion() == pytest.approx(30)


def test_update_and_removal():
    pts = [GazePoint(x, 0, 0) for x in [0, 5, 10]]
    extremes = Extremes(pts[0], pts[0], pts[0], pts[0])
    for p in pts[1:]:
        extremes.update(p)
    assert extremes.max_x.x == 10

    win = GazeStream()
    for p in pts:
        win.add(p)
    removed = win.pop_first()
    extremes.check_removal(removed, win)
    assert extremes.min_x.x == 5
    assert removed == pts[0]
