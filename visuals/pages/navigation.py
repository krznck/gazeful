from PyQt6.QtWidgets import QListWidgetItem
from PyQt6.QtWidgets import QStackedWidget

from AppContext import AppContext
from visuals.customized_widgets.CustomSidebar import CustomSidebar
from visuals.pages.MainPage import MainPage
from visuals.pages.Page import Page
from visuals.pages.VisualizerPage import VisualizerPage


def generate_navigation(context: AppContext) -> tuple[CustomSidebar, QStackedWidget]:
    PAGES: list[Page] = [MainPage(context), VisualizerPage(context)]

    navbar = CustomSidebar()
    pages = QStackedWidget()

    for page in PAGES:
        item = QListWidgetItem()
        item.setText(page.windowTitle())
        if page.icon is not None:
            item.setIcon(page.icon)
        navbar.addItem(item)
        pages.addWidget(page)

    navbar.setCurrentRow(0)
    navbar.currentRowChanged.connect(pages.setCurrentIndex)
    return navbar, pages
