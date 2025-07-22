import matplotlib.pyplot as plt
import pytest

from debug import debug_time
from debug import get_sample_image
from debug import ingest_sample
from processing.algorithms.OculomotorAnalyzer import OculomotorAnalyzer
from processing.Definitions import Definitions
from processing.GazeStream import GazeStream
from visualizing.configuration.GazePlotConfiguration import GazePlotConfiguration
from visualizing.configuration.Metadata import Metadata
from visualizing.GazePlotStrategy import GazePlotStrategy

confs = GazePlotConfiguration(None, 400)


class DummyGaze(GazeStream):
    def __init__(self, x, y, d):
        self._c = (x, y)
        self._d = d

    def centroid(self):
        return self._c

    def duration(self):
        return self._d


# NOTE: These are here just for testing performance,
# as well as visually checking results with `-m visual`
def check_sample(sample: str):
    stream = ingest_sample(sample)
    strategy = GazePlotStrategy(confs)
    defs = Definitions()
    analyzer = OculomotorAnalyzer(stream, defs)
    fixations = analyzer.extract_fixations()
    strategy.visualize(fixations, Metadata(stream.duration(), defs))


def test_one_fix_sample():
    debug_time(lambda: check_sample("one_fix"))


def test_ars_technica_sample():
    debug_time(lambda: check_sample("ars_technica"))


def test_balatro_sample():
    debug_time(lambda: check_sample("balatro"))


@pytest.mark.visual
def test_ars_technica_visual():
    confs.background_image.update(get_sample_image("ars_technica"))
    confs.legend.update(False)
    confs.metadata.update(False)
    test_ars_technica_sample()
    plt.show()
