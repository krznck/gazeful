import os
from pathlib import Path
from time import perf_counter

import matplotlib.pyplot as plt
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices
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
from visualizing.visualization_selector import create_visualizer
from visualizing.visualization_selector import VisualizationsEnum
from visualizing.VisualizationStrategy import VisualizationStrategy
from visuals.assets.icon_selector import IconsEnum
from visuals.customized_widgets.CustomComboBox import CustomComboBox
from visuals.customized_widgets.CustomPushButton import CustomPushButton
from visuals.customized_widgets.Header import Header
from visuals.pages.Page import Page
from visuals.visualization_configurations.BaseConfigurationEditor import (
    BaseConfigurationEditor,
)

TITLE = "Analysis"
ICON = IconsEnum.MICROSCOPE

REFRESH_LABEL = "Refresh"
EXPLORER_DIALOG_TEXT = "Select Gaze CSV"
EXPLORER_FILTER_STRING = "CSV Files (*.csv)"

IMPORT_TIME_LABEL = "Import time: "
DURATION_LABEL = "Session duration: "
ANALYSIS_TIME_LABEL = "Analysis time: "

CLOSURES_SECTION_HEADER = "Closures"
CLOSURES_SECTION_BLINKS = "Blink count: "
CLOSURES_SECTION_MICROSLEEPS = "Microsleep count: "

OCULOMOTOR_SECTION_HEADER = "Oculomotor behavior"
OCULOMOTOR_SECTION_FIXATION_COUNT = "Fixation count: "
OCULOMOTOR_SECTION_FIXATION_AVG = "Average fixation duration: "
OCULOMOTOR_SECTION_FIXATION_MED = "Median fixation duration: "

GENERATE_BUTTON_TEXT = "Generate"


class AnalysisPage(Page):
    refresh_buttton: QPushButton
    explorer_button: QPushButton
    path_label: QLabel
    duration_label: QLabel
    analysis_time_label: QLabel
    import_time_label: QLabel
    blink_count_label: QLabel
    visualizers_combo_box: CustomComboBox
    generate_button: CustomPushButton
    editor_button: CustomPushButton

    fixations: list[GazeStream] | None = None
    editor: BaseConfigurationEditor | None = None
    strategy: VisualizationStrategy | None = None

    def __init__(self, context: AppContext) -> None:
        super().__init__(TITLE, context, ICON)

    def add_content(self) -> None:
        self.__init_selection_section()
        self.__init_timing_section()
        self.__init_closures_section()
        self.__init_oculomotor_section()
        self.__init_visualization_section()
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

    def __init_timing_section(self) -> None:
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        hbox.addWidget(QLabel(IMPORT_TIME_LABEL))
        self.import_time_label = label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignRight)
        hbox.addWidget(label)
        vbox.addLayout(hbox)

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(ANALYSIS_TIME_LABEL))
        self.analysis_time_label = label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignRight)
        hbox.addWidget(label)
        vbox.addLayout(hbox)

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(DURATION_LABEL))
        self.duration_label = label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignRight)
        hbox.addWidget(label)
        vbox.addLayout(hbox)

        self.page_vbox.addLayout(vbox)

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

    def __init_oculomotor_section(self) -> None:
        vbox = QVBoxLayout()

        header = Header(OCULOMOTOR_SECTION_HEADER)
        vbox.addWidget(header)

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(OCULOMOTOR_SECTION_FIXATION_COUNT))
        self.fixation_count_label = QLabel()
        self.fixation_count_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        hbox.addWidget(self.fixation_count_label)
        vbox.addLayout(hbox)

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(OCULOMOTOR_SECTION_FIXATION_AVG))
        self.fixation_average_label = QLabel()
        self.fixation_average_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        hbox.addWidget(self.fixation_average_label)
        vbox.addLayout(hbox)

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(OCULOMOTOR_SECTION_FIXATION_MED))
        self.fixation_median_label = QLabel()
        self.fixation_median_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        hbox.addWidget(self.fixation_median_label)
        vbox.addLayout(hbox)

        self.page_vbox.addLayout(vbox)

    def __init_visualization_section(self) -> None:
        vbox = QVBoxLayout()

        header = Header("Visualization")
        vbox.addWidget(header)

        hbox = QHBoxLayout()

        self.visualizers_combo_box = cb = CustomComboBox()
        for vis in VisualizationsEnum:
            cb.addItem(vis.name.lower().capitalize())
        cb.setEnabled(False)

        hbox.addWidget(cb)

        self.editor_button = eb = CustomPushButton("Configure")
        eb.setEnabled(False)
        eb.clicked.connect(self.on_editor_button_clicked)
        hbox.addWidget(eb)

        self.generate_button = gb = CustomPushButton(GENERATE_BUTTON_TEXT)
        gb.setDisabled(True)
        gb.clicked.connect(self.on_generate_visualization_clicked)
        hbox.addWidget(gb)

        vbox.addLayout(hbox)

        self.page_vbox.addLayout(vbox)

    def on_explorer_button_clicked(self):
        text, _ = QFileDialog.getOpenFileName(
            self, EXPLORER_DIALOG_TEXT, "", EXPLORER_FILTER_STRING
        )

        if text != "":
            try:
                start = perf_counter()

                stream = ingest_csv(Path(text))
                self.context.main_data = stream
                end = perf_counter()
                time = end - start
                self.import_time_label.setText(f"{time:.10f} seconds")

                self.on_file_selected()
                self.path_label.setText(text)

            except InvalidFormatError as e:
                QMessageBox.warning(self, "Import warning", str(e))

    def on_file_selected(self):
        if self.context.main_data is None:
            return

        start = perf_counter()

        data = self.context.main_data
        closures = ClosureAnalyzer(self.context.main_data, self.context.defs)
        oculomotor = OculomotorAnalyzer(self.context.main_data, self.context.defs)

        fixations = self.fixations = oculomotor.extract_fixations()
        self.duration_label.setText(str(round(data.duration(), 2)) + " seconds")
        self.blink_count_label.setText(str(len(closures.extract_blinks())))
        self.microsleep_count_label.setText(str(len(closures.extract_microsleeps())))
        self.fixation_count_label.setText(str(len(fixations)))
        self.fixation_average_label.setText(
            str(round(oculomotor.average_fixation_duration(), 2)) + " ms"
        )
        self.fixation_median_label.setText(
            str(round(oculomotor.median_fixation_duration(), 2)) + " ms"
        )
        end = perf_counter()
        time = end - start
        self.analysis_time_label.setText(f"{time:.10f} seconds")

        self.refresh_buttton.setEnabled(True)
        self.visualizers_combo_box.setEnabled(True)
        self.editor_button.setEnabled(True)
        self.generate_button.setEnabled(True)

    def on_editor_button_clicked(self):
        if not self.editor:
            name = self.visualizers_combo_box.currentText().upper()
            self.configuration, self.strategy, self.editor = create_visualizer(name)

        self.editor.show()

    def on_generate_visualization_clicked(self):
        if self.fixations is None:
            return

        if not self.strategy:
            name = self.visualizers_combo_box.currentText().upper()
            self.configuration, self.strategy, self.editor = create_visualizer(name)

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Figure As...",
            filter=(
                "PNG Image (*.png);;"
                "JPEG Image (*jpg);;"
                "SVG Vector Image (*svg);;"
                "PDF Documetn (*pdf)"
            ),
        )

        if file_path:
            self.strategy.visualize(self.fixations)
            plt.savefig(
                file_path, dpi=self.configuration.dpi.value, bbox_inches="tight"
            )
            QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))
