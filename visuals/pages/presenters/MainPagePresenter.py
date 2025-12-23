from PyQt6.QtWidgets import QMessageBox
from AppContext import AppContext
from trackers.tracker_selector import TrackersEnum
from visuals.pages.MainPage import MainPage
from visuals.pages.presenters.PagePresenter import PagePresenter


class MainPagePresenter(PagePresenter[MainPage]):
    _screens_refreshing: bool

    def __init__(self, view: MainPage, context: AppContext) -> None:
        super().__init__(view, context)

        self._screens_refreshing = False
        self._init_view_state()
        self._connect_signals()

    def _init_view_state(self) -> None:
        """Sets initial state of the widgets in the view."""
        v = self._view

        selected_tracker = self._context.eyetracker
        if selected_tracker:
            for i, tracker in enumerate(TrackersEnum):
                if isinstance(selected_tracker, tracker.value):
                    v.trackers_combo_box.setCurrentIndex(i)
                    break

        is_connected = bool(selected_tracker and selected_tracker.connected())
        self._trigger_connection_toggle(on=is_connected)

        _, _, choice = self._context.check_screens_state()
        v.screens_combo_box.setCurrentIndex(choice)

    def _connect_signals(self) -> None:
        """Connects signals from the view's widgets to the presenter's slots."""
        v = self._view

        v.trackers_combo_box.currentIndexChanged.connect(
            self._on_trackers_combo_box_index_changed
        )
        v.connect_toggle.clicked.connect(self._on_connection_button_clicked)
        v.screens_combo_box.currentIndexChanged.connect(
            self._on_screens_combo_box_index_changed
        )
        v.screen_refresh_button.clicked.connect(self._on_screen_refresh_button_clicked)
        if v.visualizer_toggle:
            v.visualizer_toggle.clicked.connect(self._on_visualizer_toggle_clicked)

    def _trigger_connection_toggle(self, on: bool):
        v = self._view

        v.connect_toggle.setText("Connected" if on else "Disconnected")
        v.connect_toggle.setChecked(on)

    def _on_trackers_combo_box_index_changed(self):
        self._trigger_connection_toggle(on=False)
        self._context.disconnect_tracker()

    def _on_connection_button_clicked(self):
        v, c = self._view, self._context

        if v.connect_toggle.isChecked():
            name = v.trackers_combo_box.currentText().upper()
            result = c.connect_tracker(name)

            if not result.success:
                err = result.error
                QMessageBox.warning(v, "Disconnected", str(err))
                self._trigger_connection_toggle(on=False)
                return

            self._trigger_connection_toggle(on=True)

        else:
            c.disconnect_tracker()
            self._trigger_connection_toggle(on=False)

    def _on_screens_combo_box_index_changed(self):
        v, c = self._view, self._context

        if self._screens_refreshing:
            return

        name = v.screens_combo_box.currentText().split(": ", 1)[-1]
        result = c.specify_screen(name)

        if not result.success:
            err = result.error
            QMessageBox.warning(v, "Screen warning", str(err) + "Refreshing list.")
            v.screen_refresh_button.click()

    def _on_screen_refresh_button_clicked(self):
        v, c = self._view, self._context

        self._screens_refreshing = True

        result, names, choice = c.check_screens_state()

        v.screens_combo_box.clear()
        for index, name in enumerate(names):
            v.screens_combo_box.addItem(str(index + 1) + ": " + name)
        v.screens_combo_box.setCurrentIndex(choice)

        if not result.success:
            err = result.error
            QMessageBox.warning(v, "Screen configuration warning", err)

        self._screens_refreshing = False

    def _on_visualizer_toggle_clicked(self):
        v, c = self._view, self._context

        on = v.visualizer_toggle.isChecked()
        v.visualizer_toggle.setText(
            "Gaze visualizer: On" if on else "Gaze visualizer: Off"
        )
        c.toggle_visualizer(on)
