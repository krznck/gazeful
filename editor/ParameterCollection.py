from enum import Enum
from typing import Any

from pyqtgraph.parametertree import Parameter, ParameterTree


class ParameterEnum(Enum):
    VISUALIZATION = "Visualization"
    FIX_MIN_DURATION = "Fixation Min Duration (ms)"
    FIX_MAX_DISPERSION = "Fixation Max Dispersion (px)"
    OPACITY = "Opacity"
    GAZE_FILE = "Gaze File"
    BACKGROUND = "Background Image"
    SAVE = "Save as Image"


class ParameterError(Exception):
    """Raised when an attempt to access or manipulate a parameter is invalid."""

    pass


class ParameterCollection:
    # INFO: Despite the name, `Parameter` can be a group of parameters
    _parameters = Parameter

    def __init__(self, parameters: Parameter | None = None) -> None:
        self._parameters = parameters or self._init_parameters()
        return

    def _init_parameters(self) -> Parameter:
        params = [
            {
                "name": "Visualization",
                "type": "list",
                "limits": ["Fixation duration heatmap", "Gaze plot"],
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
        return Parameter.create(name="params", type="group", children=params)

    def connect_tree(self, tree: ParameterTree) -> None:
        tree.setParameters(param=self._parameters, showTop=False)

    def get_param(self, target: ParameterEnum) -> Parameter:
        try:
            param = self._parameters.param(target.value)  # type: ignore
            return param
        except KeyError:
            raise ParameterError(f"Could not find parameter {target.name}.")

    def get_value(self, target: ParameterEnum) -> Any:
        param = self.get_param(target)
        return param.value()

    def connect(self, target: ParameterEnum, slot) -> None:
        param = self.get_param(target)
        param.sigValueChanged.connect(slot)
