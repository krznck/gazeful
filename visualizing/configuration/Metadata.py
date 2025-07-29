from typing import Final

from processing.Definitions import Definitions


class Metadata:
    """Takes some of the metadata inherent to in creating the visualization and stores
    it as simple immutable data, letting the visualizations not care about the more
    complicated Definitions or Analyzers."""

    min_fixation_duration: Final[float]
    max_fixation_dispersion: float
    duration: float

    def __init__(self, duration: float, defs: Definitions) -> None:
        self.min_fixation_duration = defs.fixation_min_duration_ms.value
        self.max_fixation_dispersion = defs.fixation_max_dispersion_px.value
        self.duration = duration
