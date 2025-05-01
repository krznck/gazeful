from pathlib import Path

from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QPushButton

from AppContext import AppContext
from processing.GazeStream import GazeStream
from processing.ingester import ingest_csv
from processing.ingester import InvalidFormatError
from visuals.customized_widgets.CustomPushButton import CustomPushButton
from visuals.icons.icon_selector import IconsEnum
from visuals.pages.Page import Page

TITLE = "Analysis"
ICON = IconsEnum.MICROSCOPE

EXPLORER_DIALOG_TEXT = "Select Gaze CSV"
EXPLORER_FILTER_STRING = "CSV Files (*.csv)"


class AnalysisPage(Page):
    explorer_button: QPushButton
    path_label: QLabel

    def __init__(self, context: AppContext) -> None:
        super().__init__(TITLE, context, ICON)

    def add_content(self) -> None:
        self.__init_selection_section()
        return super().add_content()

    def __init_selection_section(self) -> None:
        hbox = QHBoxLayout()

        self.explorer_button = CustomPushButton(EXPLORER_DIALOG_TEXT)
        self.explorer_button.clicked.connect(self.on_explorer_button_clicked)
        hbox.addWidget(self.explorer_button)

        self.path_label = QLabel()
        hbox.addWidget(self.path_label)

        self.page_vbox.addLayout(hbox)

    def on_explorer_button_clicked(self):
        text, _ = QFileDialog.getOpenFileName(
            self, EXPLORER_DIALOG_TEXT, "", EXPLORER_FILTER_STRING
        )

        if text != "":
            try:
                # FIX: Obviously temporary, we need to do something with this
                stream = GazeStream(ingest_csv(Path(text)))
                print(stream.get_duration())

                self.path_label.setText(text)
            except InvalidFormatError as e:
                QMessageBox.warning(self, "Import warning", str(e))
