from dataclasses import dataclass


@dataclass
class Definitions:
    """Describes the threshholds and criteria for interpreting gaze data.
    For example, what counts as a fixation, blink, or saccade."""

    blink_treshhold_ms: float = 100
