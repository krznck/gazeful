from enum import Enum
from typing import Any


class HeatmapParameterEnum(Enum):
    BLUR = "Blur"
    C_MAP = "Color Map"


colormaps = [
    "turbo",
    "magma",
    "cividis",
    "inferno",
    "plasma",
    "viridis",
    "CET-L4",
]

PARAMS: list[dict[str, Any]] = [
    {
        "name": "Blur",
        "type": "slider",
        "value": 4,
        "step": 1,
        "limits": (0, 20),
        "delay": 5,
    },
    {
        "name": "Color Map",
        "type": "list",
        "limits": colormaps,
    },
]
