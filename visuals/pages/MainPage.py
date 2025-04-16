from PyQt6.QtWidgets import QComboBox
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QPushButton

import screens
from AppContext import AppContext
from trackers.tracker_selector import TrackersEnum
from visuals.customized_widgets.CustomComboBox import CustomComboBox
from visuals.customized_widgets.CustomPushButton import CustomPushButton
from visuals.icons.icon_selector import IconsEnum
from visuals.pages.Page import Page

TITLE = "Home"
ICON = IconsEnum.HOME

CONNECTION_TOGGLE_CONNECTED_TEXT: str = "Connected"
CONNECTION_TOGGLE_DISCONNECTED_TEXT: str = "Disconnected"
SCREEN_REFRESH_BUTTON_TEXT: str = "Refresh"

VISUALIZER_TOGGLE_ON_TEXT: str = "Gaze visualizer: On"
VISUALIZER_TOGGLE_OFF_TEXT: str = "Gaze visualizer: Off"


class MainPage(Page):
    trackers_combo_box: QComboBox
    screens_combo_box: QComboBox
    connect_toggle: QPushButton
    visualizer_toggle: QPushButton

    __screens_refreshing = False

    def __init__(self, context: AppContext) -> None:
        super().__init__(TITLE, context, ICON)

    def add_content(self) -> None:
        self.__init_tracker_section()
        self.__init_screens_section()
        self.__init_visualizer_section()

    def __init_tracker_section(self):
        hbox = QHBoxLayout()

        self.trackers_combo_box = CustomComboBox()
        for tracker in TrackersEnum:
            self.trackers_combo_box.addItem(tracker.name.lower().capitalize())

        self.trackers_combo_box.currentIndexChanged.connect(
            self.on_trackers_combo_box_index_changed
        )

        hbox.addWidget(self.trackers_combo_box)

        self.connect_toggle = CustomPushButton(CONNECTION_TOGGLE_DISCONNECTED_TEXT)
        self.connect_toggle.setMinimumWidth(100)  # should be same size when on and off
        self.connect_toggle.setCheckable(True)

        self.connect_toggle.clicked.connect(self.on_connection_button_clicked)

        hbox.addWidget(self.connect_toggle)

        self.page_vbox.addLayout(hbox)

    def __init_screens_section(self):
        hbox = QHBoxLayout()

        self.screens_combo_box = CustomComboBox()
        for index, name in enumerate(screens.get_screen_names()):
            self.screens_combo_box.addItem(str(index + 1) + ": " + name)

        self.screens_combo_box.currentIndexChanged.connect(
            self.on_screens_combo_box_index_changed
        )

        hbox.addWidget(self.screens_combo_box)

        self.screen_refresh_button = CustomPushButton(SCREEN_REFRESH_BUTTON_TEXT)
        self.screen_refresh_button.clicked.connect(
            self.on_screen_refresh_button_clicked
        )

        hbox.addWidget(self.screen_refresh_button)

        self.page_vbox.addLayout(hbox)

    def __init_visualizer_section(self):
        hbox = QHBoxLayout()

        self.visualizer_toggle = CustomPushButton(VISUALIZER_TOGGLE_OFF_TEXT)
        self.visualizer_toggle.setCheckable(True)
        self.visualizer_toggle.clicked.connect(self.on_visualizer_toggle_clicked)

        hbox.addWidget(self.visualizer_toggle)

        self.page_vbox.addLayout(hbox)

    def on_trackers_combo_box_index_changed(self):
        self.trigger_connection_toggle(on=False)
        self.context.disconnect_tracker()

    def on_connection_button_clicked(self):
        if self.connect_toggle.isChecked():
            name = self.trackers_combo_box.currentText().upper()
            result = self.context.connect_tracker(name)

            if not result.success:
                err = result.error
                QMessageBox.warning(self, CONNECTION_TOGGLE_DISCONNECTED_TEXT, str(err))
                self.trigger_connection_toggle(on=False)

            self.trigger_connection_toggle(on=True)

        else:
            self.context.disconnect_tracker()
            self.trigger_connection_toggle(on=False)

    def on_screens_combo_box_index_changed(self):
        if self.__screens_refreshing:
            return

        name = self.screens_combo_box.currentText().split(": ", 1)[-1]
        result = self.context.specify_screen(name)

        if not result.success:
            err = result.error
            QMessageBox.warning(self, "Screen warning", str(err) + "Refreshing list.")
            self.screen_refresh_button.click()

    def on_screen_refresh_button_clicked(self):
        self.__screens_refreshing = True

        result, names, choice = self.context.check_screens_state()

        self.screens_combo_box.clear()
        for index, name in enumerate(names):
            self.screens_combo_box.addItem(str(index + 1) + ": " + name)
        self.screens_combo_box.setCurrentIndex(choice)

        if not result.success:
            err = result.error
            QMessageBox.warning(self, "Screen configuration warning", err)

        self.__screens_refreshing = False

    def on_visualizer_toggle_clicked(self):
        on = self.visualizer_toggle.isChecked()
        self.visualizer_toggle.setText(
            VISUALIZER_TOGGLE_ON_TEXT if on else VISUALIZER_TOGGLE_OFF_TEXT
        )
        self.context.toggle_visualizer(on)

    def trigger_connection_toggle(self, on: bool):
        self.connect_toggle.setText(
            CONNECTION_TOGGLE_CONNECTED_TEXT
            if on
            else CONNECTION_TOGGLE_DISCONNECTED_TEXT
        )
        self.connect_toggle.setChecked(on)
