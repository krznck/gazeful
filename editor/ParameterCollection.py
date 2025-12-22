from enum import Enum
from typing import Any

from pyqtgraph.parametertree import Parameter, ParameterTree


class ParameterError(Exception):
    """Raised when an attempt to access or manipulate a parameter is invalid."""

    pass


class ParameterCollection:
    # NOTE: Despite the name, `Parameter` can be a group of parameters
    # NOTE: The root parameter should be a group of groups.
    # This is important for the getter behavior.
    _parameters = Parameter

    def __init__(self, parameters: Parameter) -> None:
        self._parameters = parameters

    def connect_tree(self, tree: ParameterTree) -> None:
        tree.setParameters(param=self._parameters, showTop=False)

    # NOTE: Feels dirty to accept just any Enums here.
    # But well, this makes it easier, and it's fine to utilize Python's dynamic typing
    # sometimes.
    def get_param(self, target: Enum) -> Parameter:
        key = target.value
        for group in self._parameters.children():  # type: ignore
            if key in group.names:
                return group.child(key)

        raise ParameterError(f"Could not find parameter {target.name}.")

    def get_value(self, target: Enum) -> Any:
        param = self.get_param(target)
        return param.value()

    def connect(self, target: Enum, slot) -> None:
        param = self.get_param(target)

        if param.opts["type"] == "action":
            param.sigActivated.connect(slot)  # type: ignore
            return

        param.sigValueChanged.connect(slot)
