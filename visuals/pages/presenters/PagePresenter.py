"""Base class for all page presenters following the MVP pattern."""
from abc import ABC
from typing import Generic, TypeVar

from AppContext import AppContext

from visuals.pages.Page import Page

T = TypeVar("T", bound=Page)


class PagePresenter(ABC, Generic[T]):
    """Abstract base class for page presenters.

    Coordinates between the global AppContext and a specific Page view.

    Attributes:
        _context: The application-wide state and service container.
        _view: The specific Page view managed by this presenter.
    """

    _context: AppContext
    _view: T

    def __init__(self, view: T, context: AppContext) -> None:
        """Initializes the presenter.

        Args:
            view: The view instance to manage.
            context: The application context.
        """
        self._context = context
        self._view = view
