import matplotlib.pyplot as plt
import pytest

from debug import debug_time
from debug import get_sample_image
from debug import ingest_sample
from debug import Samples
from processing.algorithms.OculomotorAnalyzer import OculomotorAnalyzer
from processing.Definitions import Definitions
from processing.GazeRecording import GazeRecording
from processing.GazeStream import GazeStream
from visualizing.configuration.GazePlotConfiguration import GazePlotConfiguration
from visualizing.configuration.Metadata import Metadata
from visualizing.GazePlotStrategy import GazePlotStrategy

confs = GazePlotConfiguration(None, 400)


# NOTE: These are here just for testing performance,
# as well as visually checking results with `-m visual`
def prepare_sample(sample: str):
    recording = ingest_sample(sample)
    defs = Definitions()
    analyzer = OculomotorAnalyzer(recording, defs)
    return analyzer.extract_fixations(), recording, defs


def check_visualization(
    fixs: list[GazeStream],
    recording: GazeRecording,
    defs: Definitions,
    conf: GazePlotConfiguration,
):
    strategy = GazePlotStrategy(conf)
    strategy.visualize(fixs, Metadata(recording.data.duration(), defs))


@pytest.mark.perf
def test_perf():
    for sample in Samples:
        args = prepare_sample(sample.value)
        debug_time(
            func=lambda: check_visualization(*args, GazePlotConfiguration(args[1])),
            message=f"{sample.value} fixation count heatmap",
        )


@pytest.mark.visual
def test_ars_technica_visual():
    args = prepare_sample(Samples.ARS.value)
    confs = GazePlotConfiguration(args[1])
    confs.background_image.update(get_sample_image(Samples.ARS.value))
    confs.legend.update(False)
    confs.metadata.update(False)
    check_visualization(*args, confs)
    plt.show()
