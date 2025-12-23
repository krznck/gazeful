from PyQt6.QtWidgets import QListWidgetItem
from PyQt6.QtWidgets import QStackedWidget

from AppContext import AppContext
from editor.EditorPage import EditorPage
from editor.EditorPresenter import EditorPresenter
from visuals.customized_widgets.CustomSidebar import CustomSidebar
from visuals.pages.MainPage import MainPage
from visuals.pages.RecordingPage import RecordingPage
from visuals.pages.VisualizerPage import VisualizerPage
from visuals.pages.presenters.MainPagePresenter import MainPagePresenter
from visuals.pages.presenters.RecordingPresenter import RecordingPresenter
from visuals.pages.presenters.VisualizerPresenter import VisualizerPresenter
import os

PAGES = [
    (MainPagePresenter, MainPage),
    (VisualizerPresenter, VisualizerPage),
    (RecordingPresenter, RecordingPage),
    (EditorPresenter, EditorPage),
]


def generate_navigation(context: AppContext) -> tuple[CustomSidebar, QStackedWidget]:
    navbar = CustomSidebar()
    pages = QStackedWidget()

    for PresenterClass, PageClass in PAGES:
        # Wayland does not allow for anything but the compositor to change the
        # positioning of an application, so the Gaze Visualizer does not work
        if type(PageClass()) == VisualizerPage and os.environ.get("WAYLAND_DISPLAY"):
            continue

        page = PageClass()
        presenter = PresenterClass(view=page, context=context)

        # NOTE: The only reason to connect the presenter to the page here is to prevent
        # it from being garbage collected. There is otherwise no reason for the page to
        # have access to its presenter, so I don't even give it an attribute for that
        # In other words, WARN: page.presenter should never be accessed
        page.presenter = presenter  # type: ignore

        item = QListWidgetItem()
        item.setText(page.windowTitle())
        if page.icon is not None:
            item.setIcon(page.icon)
        navbar.addItem(item)
        pages.addWidget(page)

    navbar.setCurrentRow(0)
    navbar.currentRowChanged.connect(pages.setCurrentIndex)
    return navbar, pages
