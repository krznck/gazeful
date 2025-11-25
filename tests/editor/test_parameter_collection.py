from types import SimpleNamespace
from typing import cast

from pyqtgraph.parametertree.Parameter import Parameter
import pytest
from editor.ParameterCollection import (
    ParameterCollection,
    ParameterEnum,
    ParameterError,
)


def test_getting_parameter_returns_on_enum():
    col = ParameterCollection()
    op = col.get_param(ParameterEnum.OPACITY)
    assert op == col._parameters.param("Opacity")  # type: ignore


def test_getting_parameters_raises_on_nonexistant():
    col = ParameterCollection()

    mock = SimpleNamespace(name="WRONG", value="NotAParamater")
    mock = cast(ParameterEnum, mock)

    with pytest.raises(ParameterError):
        col.get_param(mock)


def test_contains_base_parameters():
    col = ParameterCollection()

    for param in ParameterEnum:
        col.get_param(param)


def test_can_connect_signal():
    col = ParameterCollection()

    received = []

    def spy_slot(value):
        received.append(value)

    param = col.get_param(ParameterEnum.OPACITY)
    col.connect(ParameterEnum.OPACITY, spy_slot)
    param.sigValueChanged.emit(123, None)
    assert received == [123]


def test_returns_parameter_value():
    mock_enum = SimpleNamespace(name="MOCK", value="Mock")
    mock_enum = cast(ParameterEnum, mock_enum)
    mock_param = [{"name": "Mock", "type": "bool", "value": True}]
    mock_param = Parameter.create(name="param", type="group", children=mock_param)

    col = ParameterCollection(parameters=mock_param)

    assert col.get_value(mock_enum)
