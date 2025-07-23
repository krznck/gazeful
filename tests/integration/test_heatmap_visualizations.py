import matplotlib.pyplot as plt
import pytest

from debug import debug_time
from debug import get_sample_image
from debug import ingest_sample
from processing.algorithms.OculomotorAnalyzer import OculomotorAnalyzer
from processing.Definitions import Definitions
from visualizing.configuration.BaseConfiguration import BaseConfiguration
from visualizing.configuration.Metadata import Metadata
from visualizing.FixationCountHeatmapStrategy import FixationCountHeatmapStrategy

confs = BaseConfiguration()


def check_sample(sample: str):
    stream = ingest_sample(sample)
    strategy = FixationCountHeatmapStrategy(confs)
    defs = Definitions()
    analyzer = OculomotorAnalyzer(stream, defs)
    fixations = analyzer.extract_fixations()
    strategy.visualize(fixations, Metadata(stream.duration(), defs))


def test_ars_technica_sample():
    debug_time(lambda: check_sample("ars_technica"))


@pytest.mark.visual
def test_ars_technica_visual():
    confs.background_image.update(get_sample_image("ars_technica"))
    confs.legend.update(False)
    confs.metadata.update(False)
    test_ars_technica_sample()
    plt.show()
