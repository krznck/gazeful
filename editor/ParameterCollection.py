"""Management of hierarchical parameters for visualization settings."""

from enum import Enum
from typing import Any, Callable

from pyqtgraph.parametertree import Parameter, ParameterTree


class ParameterError(Exception):
    """Raised on invalid access or manipulation of a parameter."""

    pass


class ParameterCollection:
    """Wrapper for pyqtgraph's Parameter to simplify access and signal binding.

    This class provides a flat interface for accessing parameters nested within a
    hierarchical group structure.

    Attributes:
        _parameters: The root Parameter group containing all settings.
    """

    _parameters: Parameter

    def __init__(self, parameters: Parameter) -> None:
        """Initializes the collection.

        Args:
            parameters: The root Parameter group.
        """
        self._parameters = parameters

    def connect_tree(self, tree: ParameterTree) -> None:
        """Attaches the parameter collection to a UI tree view.

        Args:
            tree: The ParameterTree widget to display these parameters.
        """
        tree.setParameters(param=self._parameters, showTop=False)

    def get_param(self, target: Enum) -> Parameter:
        """Retrieves a specific Parameter object by its Enum key.

        Args:
            target: The Enum member representing the parameter.

        Returns:
            The corresponding pyqtgraph Parameter object.

        Raises:
            ParameterError: If the parameter key is not found in any child group.
        """
        key = target.value
        for group in self._parameters.children():  # type: ignore
            if key in group.names:
                return group.child(key)

        raise ParameterError(f"Could not find parameter {target.name}.")

    def get_value(self, target: Enum) -> Any:
        """Retrieves the current value of a parameter.

        Args:
            target: The Enum member representing the parameter.

        Returns:
            The current value stored in the parameter.
        """
        param = self.get_param(target)
        return param.value()

    def connect(self, target: Enum, slot: Callable[..., None]) -> None:
        """Connects a parameter's change or activation signal to a slot.

        Handles both standard value changes and 'action' type triggers.

        Args:
            target: The Enum member representing the parameter.
            slot: The callable to trigger when the parameter changes.
        """
        param = self.get_param(target)

        if param.opts["type"] == "action":
            param.sigActivated.connect(slot)  # type: ignore
            return

        param.sigValueChanged.connect(slot)
