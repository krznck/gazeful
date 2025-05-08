from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QVBoxLayout

from AppContext import AppContext
from processing.algorithms.ClosureAnalyzer import ClosureAnalyzer
from processing.algorithms.OculomotorAnalyzer import OculomotorAnalyzer
from processing.GazeStream import GazeStream
from processing.ingester import ingest_csv
from processing.ingester import InvalidFormatError
from visuals.customized_widgets.CustomPushButton import CustomPushButton
from visuals.customized_widgets.Header import Header
from visuals.icons.icon_selector import IconsEnum
from visuals.pages.Page import Page

TITLE = "Analysis"
ICON = IconsEnum.MICROSCOPE

REFRESH_LABEL = "Refresh"
EXPLORER_DIALOG_TEXT = "Select Gaze CSV"
EXPLORER_FILTER_STRING = "CSV Files (*.csv)"

DURATION_LABEL = "Session duration: "

CLOSURES_SECTION_HEADER = "Closures"
CLOSURES_SECTION_BLINKS = "Blinks: "
CLOSURES_SECTION_MICROSLEEPS = "Microsleeps: "


class AnalysisPage(Page):
    refresh_buttton: QPushButton
    explorer_button: QPushButton
    path_label: QLabel
    duration_label: QLabel
    blink_count_label: QLabel

    def __init__(self, context: AppContext) -> None:
        super().__init__(TITLE, context, ICON)

    def add_content(self) -> None:
        self.__init_selection_section()
        self.__init_duration_section()
        self.__init_closures_section()
        return super().add_content()

    def __init_selection_section(self) -> None:
        hbox = QHBoxLayout()

        self.refresh_buttton = CustomPushButton(REFRESH_LABEL)
        self.refresh_buttton.clicked.connect(self.on_file_selected)
        self.refresh_buttton.setDisabled(True)
        hbox.addWidget(self.refresh_buttton)
        self.explorer_button = CustomPushButton(EXPLORER_DIALOG_TEXT)
        self.explorer_button.clicked.connect(self.on_explorer_button_clicked)
        hbox.addWidget(self.explorer_button)

        self.path_label = QLabel()
        hbox.addWidget(self.path_label)

        self.page_vbox.addLayout(hbox)

    def __init_duration_section(self) -> None:
        hbox = QHBoxLayout()

        hbox.addWidget(QLabel(DURATION_LABEL))
        self.duration_label = label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignRight)
        hbox.addWidget(label)

        self.page_vbox.addLayout(hbox)

    def __init_closures_section(self) -> None:
        vbox = QVBoxLayout()

        header = Header(CLOSURES_SECTION_HEADER)
        vbox.addWidget(header)

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(CLOSURES_SECTION_BLINKS))
        self.blink_count_label = QLabel()
        self.blink_count_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        hbox.addWidget(self.blink_count_label)
        vbox.addLayout(hbox)

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(CLOSURES_SECTION_MICROSLEEPS))
        self.microsleep_count_label = QLabel()
        self.microsleep_count_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        hbox.addWidget(self.microsleep_count_label)
        vbox.addLayout(hbox)

        self.page_vbox.addLayout(vbox)

    def on_explorer_button_clicked(self):
        text, _ = QFileDialog.getOpenFileName(
            self, EXPLORER_DIALOG_TEXT, "", EXPLORER_FILTER_STRING
        )

        if text != "":
            try:
                stream = GazeStream(ingest_csv(Path(text)))
                self.context.main_data = stream
                self.on_file_selected()

                self.path_label.setText(text)
            except InvalidFormatError as e:
                QMessageBox.warning(self, "Import warning", str(e))

    def on_file_selected(self):
        if self.context.main_data is None:
            return

        self.refresh_buttton.setEnabled(True)
        data = self.context.main_data
        closures = ClosureAnalyzer(self.context.main_data, self.context.defs)
        oculomotor = OculomotorAnalyzer(self.context.main_data, self.context.defs)
        self.duration_label.setText(str(round(data.get_duration(), 2)) + " seconds")
        self.blink_count_label.setText(str(len(closures.extract_blinks())))
        self.microsleep_count_label.setText(str(len(closures.extract_microsleeps())))
        print(len(oculomotor.extract_fixations()))
