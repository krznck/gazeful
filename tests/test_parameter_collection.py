"""Unit tests for the ParameterCollection wrapper."""
from enum import Enum
from types import SimpleNamespace
from typing import cast

import pytest
from editor.ParameterCollection import ParameterCollection, ParameterError
from pyqtgraph.parametertree.Parameter import Parameter


class MockEnum(Enum):
    """Simple enum for mocking parameter keys."""
    MOCK = "Mock"


def setup():
    """Sets up a nested pyqtgraph parameter structure for testing."""
    leaf = {"name": "Mock", "type": "bool", "value": True}
    group = Parameter.create(name="Group", type="group", children=[leaf])
    root = Parameter.create(name="Root", type="group", children=[group])
    return root


def test_getting_parameter_returns_on_enum():
    col = ParameterCollection(setup())
    op = col.get_param(MockEnum.MOCK)
    assert op.name() == "Mock" and op.value() is True and op.type() == "bool"


def test_getting_parameters_raises_on_nonexistant():
    col = ParameterCollection(setup())

    # Not the same enum as what's in Parameter
    mock = SimpleNamespace(name="WRONG", value="NotAParamater")
    mock = cast(Enum, mock)

    with pytest.raises(ParameterError):
        col.get_param(mock)


def test_can_connect_signal():
    col = ParameterCollection(setup())

    received = []

    def spy_slot(value):
        received.append(value)

    param = col.get_param(MockEnum.MOCK)
    col.connect(MockEnum.MOCK, spy_slot)
    param.sigValueChanged.emit(123, None)
    assert received == [123]


def test_returns_parameter_value():
    col = ParameterCollection(setup())

    assert col.get_value(MockEnum.MOCK) is True
