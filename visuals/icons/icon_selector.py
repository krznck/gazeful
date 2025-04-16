from enum import Enum

from PyQt6.QtGui import QIcon

PATH = "assets/fluentui-system-icons/"


class IconsEnum(Enum):
    HOME = "ic_fluent_home_24_regular.svg"
    CIRCLE = "ic_fluent_circle_24_regular.svg"


def create_icon(choice: IconsEnum) -> QIcon:
    return QIcon(PATH + choice.value)
