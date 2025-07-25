import matplotlib.pyplot as plt
import pytest

from debug import debug_time
from debug import get_sample_image
from debug import ingest_sample
from debug import Samples
from processing.algorithms.OculomotorAnalyzer import OculomotorAnalyzer
from processing.Definitions import Definitions
from processing.GazeStream import GazeStream
from visualizing.configuration.GazePlotConfiguration import GazePlotConfiguration
from visualizing.configuration.Metadata import Metadata
from visualizing.GazePlotStrategy import GazePlotStrategy

confs = GazePlotConfiguration(None, 400)


# NOTE: These are here just for testing performance,
# as well as visually checking results with `-m visual`
def prepare_sample(sample: str):
    stream = ingest_sample(sample)
    defs = Definitions()
    analyzer = OculomotorAnalyzer(stream, defs)
    return analyzer.extract_fixations(), stream, defs


def check_visualization(fixs: list[GazeStream], data: GazeStream, defs: Definitions):
    strategy = GazePlotStrategy(confs)
    strategy.visualize(fixs, Metadata(data.duration(), defs))


@pytest.mark.perf
def test_perf():
    for sample in Samples:
        args = prepare_sample(sample.value)
        debug_time(
            func=lambda: check_visualization(*args),
            message=f"{sample.value} gaze sequence map",
        )


@pytest.mark.visual
def test_ars_technica_visual():
    confs.background_image.update(get_sample_image(Samples.ARS.value))
    confs.legend.update(False)
    confs.metadata.update(False)
    check_visualization(*prepare_sample(Samples.ARS.value))
    plt.show()
