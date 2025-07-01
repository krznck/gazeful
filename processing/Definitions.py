from dataclasses import dataclass

from Ref import Ref


@dataclass
class Definitions:
    """Describes the threshholds and criteria for interpreting gaze data.
    For example, what counts as a fixation, blink, or saccade.
    NOTE: Uses Ref objects to enable data-binding."""

    blink_threshhold_ms: Ref[float] = Ref(400)
    fixation_minimum_duration_ms: Ref[float] = Ref(200)
    fixation_maximum_dispersion_screen_area_percent: Ref[float] = Ref(0.05)
