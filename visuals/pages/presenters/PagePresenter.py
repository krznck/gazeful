from abc import ABC
from typing import Generic, TypeVar
from AppContext import AppContext
from visuals.pages.Page import Page

T = TypeVar("T", bound=Page)


class PagePresenter(ABC, Generic[T]):
    _context: AppContext
    _view: T

    def __init__(self, view: T, context: AppContext) -> None:
        self._context = context
        self._view = view
