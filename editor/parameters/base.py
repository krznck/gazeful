"""
Dictionary representing common parameters - parameters that every visualization should
be able to utilize.
"""

from enum import Enum
from typing import Any
from editor.visualization.VisualizationKind import VisualizationKind


class ParameterEnum(Enum):
    VISUALIZATION = "Visualization"
    FIX_MIN_DURATION = "Fixation Min Duration (ms)"
    FIX_MAX_DISPERSION = "Fixation Max Dispersion (px)"
    OPACITY = "Opacity"
    GAZE_FILE = "Gaze File"
    BACKGROUND = "Background Image"
    SAVE = "Save as Image"


PARAMS: list[dict[str, Any]] = [
    {
        "name": "Visualization",
        "type": "list",
        "limits": [kind.value for kind in VisualizationKind],
    },
    {
        "name": "Fixation Min Duration (ms)",
        "type": "float",
        "value": 200,
        "step": 10,
        "limits": (0, 1000),
    },
    {
        "name": "Fixation Max Dispersion (px)",
        "type": "float",
        "value": 65,
        "step": 1,
        "limits": (0, 500),
    },
    {
        "name": "Opacity",
        "type": "slider",
        "value": 0.8,
        "step": 0.05,
        "limits": (0, 1),
    },
    {
        "name": "Gaze File",
        "type": "file",
        "winTitle": "Select Gaze CSV",
        "nameFilter": "CSV Files (*.csv)",
        "value": "",
    },
    {
        "name": "Background Image",
        "type": "file",
        "winTitle": "Select background image",
        "nameFilter": "Images (*.png *.jpg *.jpeg *.bmp *.webp)",
        "value": "",
    },
    {
        "name": "Save as Image",
        "type": "action",
    },
]
