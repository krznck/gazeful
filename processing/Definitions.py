from dataclasses import dataclass


class Ref:
    """Wrapper for a primitive value, allowing it to be passed by reference."""

    def __init__(self, value):
        self.value = value

    def update(self, value):
        self.value = value


@dataclass
class Definitions:
    """Describes the threshholds and criteria for interpreting gaze data.
    For example, what counts as a fixation, blink, or saccade.
    NOTE: Uses Ref objects to enable data-binding."""

    blink_threshhold_ms = Ref(100)
    fixation_minimum_duration_ms = Ref(200)
    fixation_maximum_dispersion_screen_area_percent = Ref(0.05)
