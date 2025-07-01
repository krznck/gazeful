import matplotlib.pyplot as plt
import numpy as np
import pytest

from debug import ingest_sample
from processing.algorithms.OculomotorAnalyzer import OculomotorAnalyzer
from processing.Definitions import Definitions
from processing.GazeStream import GazeStream
from visualizing.configuration.GazePlotConfiguration import GazePlotConfiguration
from visualizing.GazePlotStrategy import GazePlotStrategy

confs = GazePlotConfiguration(1920, 1200)


class DummyGaze(GazeStream):
    def __init__(self, x, y, d):
        self._c = (x, y)
        self._d = d

    def centroid(self):
        return self._c

    def duration(self):
        return self._d


def test_visualize_simple():
    data = [
        DummyGaze(0.5, 0.5, 0.25),
        DummyGaze(0.75, 0.65, 0.5),
        DummyGaze(0.91, 0.87, 1.5),
    ]
    strategy = GazePlotStrategy(confs)
    _, axes = strategy.visualize(data)

    cols = axes.collections
    assert len(cols) == 1  # one scatter collection

    coll = cols[0]
    offsets = coll.get_offsets()

    # data points are scaled by screen dims
    sw = confs.screen_width.value
    sh = confs.screen_height.value
    expected = np.array(
        [
            (0.5 * sw, sh - 0.5 * sh),
            (0.75 * sw, sh - 0.65 * sh),
            (0.91 * sw, sh - 0.87 * sh),
        ]
    )
    assert np.allclose(offsets, expected)


def check_sample(sample: str):
    stream = ingest_sample(sample)
    strategy = GazePlotStrategy(confs)
    analyzer = OculomotorAnalyzer(stream, Definitions())
    fixations = analyzer.extract_fixations()
    _, axes = strategy.visualize(fixations)

    cols = axes.collections
    assert len(cols) == 1

    coll = cols[0]
    offsets = np.asarray(coll.get_offsets())

    assert len(fixations) == len(offsets)

    # check where the data points should be
    sw = confs.screen_width.value
    sh = confs.screen_height.value
    expected = np.array(
        [
            (
                f.centroid()[0] * sw,
                sh - f.centroid()[1] * sh,
            )
            for f in fixations
        ]
    )

    # plt.show()
    assert np.allclose(offsets, expected)


def test_one_fix_sample():
    check_sample("one_fix")


def test_ars_technica_sample():
    check_sample("ars_technica")


def test_balatro_sample():
    check_sample("balatro")


@pytest.mark.visual
def test_ars_technica_visual():
    test_ars_technica_sample()
    plt.show()
