from enum import Enum

from PyQt6.QtGui import QIcon

PATH = "assets/icons/"


class IconsEnum(Enum):
    HOME = "ic_fluent_home_24_regular.svg"
    CIRCLE = "ic_fluent_circle_24_regular.svg"
    RECORD = "ic_fluent_record_24_regular.svg"
    MICROSCOPE = "ic_fluent_microscope_24_regular.svg"
    BOOK_INFO = "ic_fluent_book_information_24_regular.svg"


def create_icon(choice: IconsEnum) -> QIcon:
    return QIcon(PATH + choice.value)
