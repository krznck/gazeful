from PyQt6.QtWidgets import QListWidgetItem
from PyQt6.QtWidgets import QStackedWidget

from AppContext import AppContext
from visuals.customized_widgets.CustomSidebar import CustomSidebar
from visuals.pages.MainPage import MainPage
from visuals.pages.RecordingPage import RecordingPage
from visuals.pages.VisualizerPage import VisualizerPage

PAGES = [MainPage, VisualizerPage, RecordingPage]


def generate_navigation(context: AppContext) -> tuple[CustomSidebar, QStackedWidget]:
    navbar = CustomSidebar()
    pages = QStackedWidget()

    for PageClass in PAGES:
        page = PageClass(context)
        item = QListWidgetItem()
        item.setText(page.windowTitle())
        if page.icon is not None:
            item.setIcon(page.icon)
        navbar.addItem(item)
        pages.addWidget(page)

    navbar.setCurrentRow(0)
    navbar.currentRowChanged.connect(pages.setCurrentIndex)
    return navbar, pages
