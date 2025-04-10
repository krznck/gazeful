from PyQt6.QtGui import QGuiApplication
from PyQt6.QtGui import QScreen


def get_screen_names() -> list[str]:
    screens = QGuiApplication.screens()
    screen_strings: list[str] = []
    for screen in screens:
        screen_strings.append(screen.name())

    return screen_strings


def get_primary_screen() -> QScreen:
    screen = QGuiApplication.primaryScreen()
    if screen is None:
        raise HeadlessError("Running headless - no primary screen detected.")
    return screen


def get_index(target: QScreen) -> int:
    screens = QGuiApplication.screens()
    for i in range(len(screens)):
        if screens[i].name == target.name:
            return i

    raise InvalidScreenBinding("Cannot find the monitor requested.")


def get_screen(target: int | str) -> QScreen:
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
    screen_geo = screen.geometry()
    return screen_geo.width(), screen_geo.height()


def get_geometry(screen: QScreen) -> tuple[int, int, float, float]:
    """Returns the geometry of the screen as a tuple.
    This is mostly to simplify process of harvesting geometry() return values."""
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
