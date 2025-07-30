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
from visualizing.AbsolueGazeDurationHeatmapStrategy import (
    AbsoluteGazeDurationHeatmapStrategy,
)
from visualizing.configuration.HeatmapConfiguration import HeatmapConfiguration
from visualizing.configuration.Metadata import Metadata
from visualizing.FixationCountHeatmapStrategy import FixationCountHeatmapStrategy


def prepare_sample(sample: str):
    recording = ingest_sample(sample)
    defs = Definitions()
    analyzer = OculomotorAnalyzer(recording, defs)
    return analyzer.extract_fixations(), recording, defs


def check_fixation_count(
    fixs: list[GazeStream],
    recording: GazeRecording,
    defs: Definitions,
    conf: HeatmapConfiguration,
):
    strategy = FixationCountHeatmapStrategy(conf)
    strategy.visualize(fixs, Metadata(recording.data.duration(), defs))


def check_absolute_gaze_duration(
    fixs: list[GazeStream],
    recording: GazeRecording,
    defs: Definitions,
    conf: HeatmapConfiguration,
):
    strategy = AbsoluteGazeDurationHeatmapStrategy(conf)
    strategy.visualize(fixs, Metadata(recording.data.duration(), defs))


@pytest.mark.perf
def test_perf():
    for sample in Samples:
        args = prepare_sample(sample.value)
        debug_time(
            func=lambda: check_absolute_gaze_duration(
                *args, HeatmapConfiguration(args[1])
            ),
            message=f"{sample.value} fixation count heatmap",
        )
        debug_time(
            func=lambda: check_fixation_count(*args, HeatmapConfiguration(args[1])),
            message=f"{sample.value} absolute gaze duration heatmap",
        )


@pytest.mark.visual
def test_ars_technica_visual():
    args = prepare_sample(Samples.ARS.value)
    confs = HeatmapConfiguration(args[1])
    confs.background_image.update(get_sample_image(Samples.ARS.value))
    confs.legend.update(False)
    confs.metadata.update(False)
    check_absolute_gaze_duration(*args, confs)
    plt.show()
    check_fixation_count(*args, confs)
    plt.show()
