"""Parameters specific to gaze plot visualizations."""
from enum import Enum
from typing import Any


class GazePlotParameterEnum(Enum):
    """Enums representing the unique names of gaze plot-specific parameters."""

    FIX_COLOR = "Fixation color"
    CON_COLOR = "Connection color"
    HOV_COLOR = "Hover color"
    ADJ_COLOR = "Adjacent color"
    ANTIALIAS = "Antialiasing"


PARAMS: list[dict[str, Any]] = [
    {
        "name": "Fixation color",
        "type": "color",
        "value": "blue",
    },
    {
        "name": "Connection color",
        "type": "color",
        "value": "blue",
    },
    {
        "name": "Hover color",
        "type": "color",
        "value": "yellow",
    },
    {
        "name": "Adjacent color",
        "type": "color",
        "value": "orange",
    },
    {
        "name": "Antialiasing",
        "type": "bool",
        "value": False,
    },
]
