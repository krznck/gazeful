from pyqtgraph.parametertree import Parameter
from pyqtgraph.parametertree.ParameterTree import ParameterTree


class ParameterError(Exception):
    """Raised when an attempt to access or manipulate a parameter is invalid."""

    pass


class CommonParameterTree(ParameterTree):
    _parameters = Parameter

    def __init__(self, parent=None, showHeader=True):
        super().__init__(parent, showHeader)
        self._parameters = self._init_parameters()
        self.setParameters(self._parameters, showTop=False)

    def get_param(self, name: str) -> Parameter:
        param = self._parameters.param(name)  # type: ignore
        if param:
            return param
        else:
            raise ParameterError(f"Could not find parameter {name}.")

    def _init_parameters(self) -> Parameter:
        params = [
            {
                "name": "Visualization",
                "type": "list",
                "limits": ["Fixation duration heatmap", "Gaze plot"],
            },
            # {
            #     "name": "Fixation Min Duration (ms)",
            #     "type": "float",
            #     "value": self.defs.fixation_min_duration_ms.value,
            #     "step": 10,
            #     "limits": (0, 1000),
            # },
            # {
            #     "name": "Fixation Max Dispersion (px)",
            #     "type": "float",
            #     "value": self.defs.fixation_max_dispersion_px.value,
            #     "step": 1,
            #     "limits": (0, 500),
            # },
            {
                "name": "Opacity",
                "type": "slider",
                "value": 0.8,
                "step": 0.05,
                "limits": (0, 1),
            },
            {
                "name": "Antialiasing",
                "type": "bool",
                "value": False,
            },
            {
                "name": "Gaze CSV",
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
