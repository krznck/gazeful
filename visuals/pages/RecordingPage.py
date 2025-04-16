from AppContext import AppContext
from visuals.icons.icon_selector import IconsEnum
from visuals.pages.Page import Page

ICON = IconsEnum.RECORD
TITLE = "Recording"


class RecordingPage(Page):
    def __init__(self, context: AppContext) -> None:
        super().__init__(TITLE, context, ICON)
