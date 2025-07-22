from typing import Generic
from typing import TypeVar


Type = TypeVar("Type")


class Ref(Generic[Type]):
    """Wrapper for a primitive value, allowing it to be passed by reference."""

    def __init__(self, value: Type):
        self.value = value

    def update(self, value: Type):
        self.value = value

    def __bool__(self) -> bool:
        return bool(self.value)
