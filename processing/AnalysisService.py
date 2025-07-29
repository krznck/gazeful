from pathlib import Path

from processing.algorithms.ClosureAnalyzer import ClosureAnalyzer
from processing.algorithms.OculomotorAnalyzer import OculomotorAnalyzer
from processing.Definitions import Definitions
from processing.GazeRecording import GazeRecording
from processing.GazeStream import GazeStream
from processing.ingester import ingest_csv
from visualizing.configuration.Metadata import Metadata
from visualizing.visualization_selector import create_visualizer
from visualizing.visualization_selector import VisualizationsEnum
from visuals.visualization_configurations.BaseConfigurationEditor import (
    BaseConfigurationEditor,
)


class AnalysisService:
    def __init__(
        self,
        definitions: Definitions,
        data: GazeRecording | Path,
        vis_type: VisualizationsEnum,
    ) -> None:
        match data:
            case GazeRecording() as recording:
                self._recording = recording
            case Path() as path:
                self._recording = ingest_csv(path)
        self._oculomotor = OculomotorAnalyzer(self._recording.data, definitions)
        self._closures = ClosureAnalyzer(self._recording.data, definitions)
        self._defs = definitions
        self.set_strategy(vis_type)

    # NOTE: Having this service create and hold a UI component (the editor) makes
    # it somewhat of a leaky abstraction.
    # I'm fine with it here, but not too happy about it.
    def set_strategy(self, vis_type: VisualizationsEnum):
        conf, self._strategy, self._editor = create_visualizer(
            vis_type, self._recording
        )
        self._configuration = conf
        screen = self._recording.screen
        if screen:
            conf.screen_width.update(screen[0])
            conf.screen_height.update(screen[1])
        background = self._recording.screenshot
        if background:
            conf.background_image.update(background)

    @property
    def active_editor(self) -> BaseConfigurationEditor:
        return self._editor

    def save_visualization(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        meta = Metadata(self.session_duration, self._defs)
        fig, _ = self._strategy.visualize(self._fixations, meta)
        fig.savefig(path, dpi=self._configuration.dpi.value, bbox_inches="tight")

    @property
    def session_duration(self) -> float:
        return round(self._recording.data.duration(), 2)

    @property
    def fixation_count(self) -> int:
        return len(self._fixations)

    @property
    def fixation_average(self) -> float:
        return round(self._oculomotor.average_fixation_duration(), 2)

    @property
    def fixation_median(self) -> float:
        return round(self._oculomotor.median_fixation_duration(), 2)

    @property
    def _fixations(self) -> list[GazeStream]:
        return self._oculomotor.extract_fixations()

    @property
    def blink_count(self) -> int:
        return len(self._blinks)

    @property
    def _blinks(self) -> list[GazeStream]:
        return self._closures.extract_blinks()

    @property
    def microsleep_count(self) -> int:
        return len(self._microsleeps)

    @property
    def _microsleeps(self) -> list[GazeStream]:
        return self._closures.extract_microsleeps()
