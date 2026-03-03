"""Utilities for interacting with system monitors via Qt."""
from PyQt6.QtGui import QGuiApplication, QScreen


def get_screen_names() -> list[str]:
    """Retrieves the unique system names of all connected screens.

    Returns:
        A list of screen names.
    """
    screens = QGuiApplication.screens()
    screen_strings: list[str] = []
    for screen in screens:
        screen_strings.append(screen.name())

    return screen_strings


def get_primary_screen() -> QScreen:
    """Retrieves the primary system screen.

    Returns:
        The primary QScreen object.

    Raises:
        HeadlessError: If no primary screen is detected (e.g., running on a server).
    """
    screen = QGuiApplication.primaryScreen()
    if screen is None:
        raise HeadlessError("Running headless - no primary screen detected.")
    return screen


def get_index(target: QScreen) -> int:
    """Finds the positional index of a specific screen in the system list.

    Args:
        target: The screen to locate.

    Returns:
        The integer index of the screen.

    Raises:
        InvalidScreenBinding: If the screen cannot be found in the current list.
    """
    screens = QGuiApplication.screens()
    for i in range(len(screens)):
        if screens[i].name == target.name:
            return i

    raise InvalidScreenBinding("Cannot find the monitor requested.")


def get_screen(target: int | str) -> QScreen:
    """Retrieves a screen object by its index or name.

    Args:
        target: The index (int) or the unique name (str) of the screen.

    Returns:
        The requested QScreen object.

    Raises:
        InvalidScreenBinding: If no screen matches the given index or name.
    """
    if isinstance(target, int):
        screens = QGuiApplication.screens()
        if target > len(screens) - 1:
            raise InvalidScreenBinding("No screen with given index found.")
        return screens[target]

    screens = QGuiApplication.screens()
    for screen in screens:
        if screen.name() == target:
            return screen
    raise InvalidScreenBinding("There is no screen with the given name.")


def get_screen_size(screen: QScreen) -> tuple[int, int]:
    """Retrieves the width and height of a screen.

    Args:
        screen: The screen to measure.

    Returns:
        A tuple of (width, height).
    """
    screen_geo = screen.geometry()
    return screen_geo.width(), screen_geo.height()


def get_geometry(screen: QScreen) -> tuple[int, int, float, float]:
    """Returns the geometry of the screen as a tuple.

    This is mostly to simplify process of harvesting geometry() return values.

    Args:
        screen: The screen to query.

    Returns:
        A tuple of (x, y, width, height).
    """
    geometry = screen.geometry()

    x = geometry.x()
    y = geometry.y()
    width = geometry.width()
    height = geometry.height()
    return x, y, width, height


class InvalidScreenBinding(Exception):
    """Raised when attempting to bind to a screen that cannot be found."""

    pass


class HeadlessError(InvalidScreenBinding):
    """Raised when attempting to use a primary screen that does not exist."""

    pass
