from pathlib import Path
from time import perf_counter

from PyQt6.QtCore import Qt
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QVBoxLayout

from AppContext import AppContext
from processing.AnalysisService import AnalysisService
from processing.ingester import InvalidFormatError
from recording.validators import get_default_recording_dir
from recording.validators import get_default_visualization_dir
from recording.validators import iso_8601_date
from recording.validators import iso_8601_time
from visualizing.visualization_selector import VisualizationsEnum
from visuals.assets.icon_selector import IconsEnum
from visuals.customized_widgets.CustomComboBox import CustomComboBox
from visuals.customized_widgets.CustomPushButton import CustomPushButton
from visuals.customized_widgets.Header import Header
from visuals.pages.Page import InvalidInteractionError
from visuals.pages.Page import Page

TITLE = "Analysis"
ICON = IconsEnum.MICROSCOPE

REFRESH_LABEL = "Refresh"
EXPLORER_DIALOG_TEXT = "Select Gaze CSV"

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
    def __init__(self, context: AppContext) -> None:
        self._save_path: Path = (
            get_default_visualization_dir()
            / f"figures-{iso_8601_date()}"
            / f"figure-{iso_8601_time()}.png"
        )
        super().__init__(TITLE, context, ICON)
        self.editor = None
        self.strategy = None
        self._service: AnalysisService | None = None
        if context.main_data:
            self._service = AnalysisService(
                context.defs,
                context.main_data,
                self._visualization_choice,
            )
        context.main_data_changed.connect(self._on_data_loaded)

    def _on_data_loaded(self):
        con = self.context
        if not con.main_data:
            raise InvalidInteractionError("Attempted to load empty data.")

        self._service = AnalysisService(
            con.defs, con.main_data, self._visualization_choice
        )
        self.path_label.setText("data loaded from recording")
        self.import_time_label.setText("not applicable")
        self._on_data_selected()

    def set_save_location(self, path: str | Path):
        if isinstance(path, str):
            self._save_path = Path(path)
        elif isinstance(path, Path):
            self._save_path = path
        self.save_location_label.setText(f"Path: {path}")

    def add_content(self) -> None:
        self._init_selection_section()
        self._init_timing_section()
        self._init_closures_section()
        self._init_oculomotor_section()
        self._init_visualization_section()
        return super().add_content()

    def _init_selection_section(self) -> None:
        hbox = QHBoxLayout()

        rb = self.refresh_button = CustomPushButton(REFRESH_LABEL)
        rb.clicked.connect(self._on_data_selected)
        rb.setDisabled(True)
        hbox.addWidget(rb)
        eb = self.explorer_button = CustomPushButton(EXPLORER_DIALOG_TEXT)
        eb.clicked.connect(self._on_explorer_button_clicked)
        hbox.addWidget(eb)

        self.path_label = QLabel()
        hbox.addWidget(self.path_label)

        self.page_vbox.addLayout(hbox)

    def _init_timing_section(self) -> None:
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

    def _init_closures_section(self) -> None:
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

    def _init_oculomotor_section(self) -> None:
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

    def _init_visualization_section(self) -> None:
        vbox = QVBoxLayout()

        header = Header("Visualization")
        vbox.addWidget(header)

        hbox = QHBoxLayout()

        self.visualizers_combo_box = cb = CustomComboBox()
        for vis in VisualizationsEnum:
            cb.addItem(str(vis))
        cb.setEnabled(False)
        cb.currentIndexChanged.connect(self._on_visualizers_combo_box_index_changed)

        hbox.addWidget(cb)

        self.editor_button = eb = CustomPushButton("Configure")
        eb.setEnabled(False)
        eb.clicked.connect(self._on_editor_button_clicked)
        hbox.addWidget(eb)

        vbox.addLayout(hbox)

        hbox = QHBoxLayout()

        inner_vbox = QVBoxLayout()
        self.choose_save_location_button = cslb = CustomPushButton(
            "Choose save location"
        )
        cslb.setEnabled(False)
        cslb.clicked.connect(self._on_choose_save_location_button_clicked)
        inner_vbox.addWidget(cslb)
        self.save_location_label = sll = QLabel(f"Path: {self._save_path}")
        sll.setEnabled(False)
        inner_vbox.addWidget(sll)
        hbox.addLayout(inner_vbox)

        self.generate_button = gb = CustomPushButton(GENERATE_BUTTON_TEXT)
        gb.setDisabled(True)
        gb.clicked.connect(self._on_generate_visualization_clicked)
        hbox.addWidget(gb)

        vbox.addLayout(hbox)

        self.page_vbox.addLayout(vbox)

    @property
    def _visualization_choice(self) -> VisualizationsEnum:
        return list(VisualizationsEnum)[self.visualizers_combo_box.currentIndex()]

    def _on_visualizers_combo_box_index_changed(self):
        serv = self._service
        if not serv:
            raise InvalidInteractionError(
                "Attempted to change visualization type before anything has been analyzed."
            )
        serv.set_strategy(self._visualization_choice)

    def _on_explorer_button_clicked(self):
        text, _ = QFileDialog.getOpenFileName(
            self,
            caption=EXPLORER_DIALOG_TEXT,
            directory=str(get_default_recording_dir()),
            filter="CSV Files (*.csv)",
        )

        if text != "":
            try:
                start = perf_counter()
                self.context.main_data = Path(text)
                self.path_label.setText(text)
                end = perf_counter()
                time = end - start
                self.import_time_label.setText(f"{time:.10f} seconds")
            except InvalidFormatError as e:
                QMessageBox.warning(self, "Import warning", str(e))

    def _on_data_selected(self):
        if not self._service:
            raise InvalidInteractionError(
                "Attempted to analyze data that has not been chosen"
            )

        start = perf_counter()

        serv = self._service

        self.duration_label.setText(f"{serv.session_duration} seconds")
        self.blink_count_label.setText(f"{serv.blink_count} blinks")
        self.microsleep_count_label.setText(f"{serv.microsleep_count} microsleeps")
        self.fixation_count_label.setText(f"{serv.fixation_count} fixations")
        self.fixation_average_label.setText(f"{serv.fixation_average} ms")
        self.fixation_median_label.setText(f"{serv.fixation_median} ms")
        end = perf_counter()
        time = end - start
        self.analysis_time_label.setText(f"{time:.10f} seconds")

        self.refresh_button.setEnabled(True)
        self.visualizers_combo_box.setEnabled(True)
        self.editor_button.setEnabled(True)
        self.generate_button.setEnabled(True)
        self.choose_save_location_button.setEnabled(True)
        self.save_location_label.setEnabled(True)

    def _on_choose_save_location_button_clicked(self):
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
        self.set_save_location(file_path)

    def _on_editor_button_clicked(self):
        serv = self._service
        if not serv:
            raise InvalidInteractionError(
                "Attempted to edit a configuration that hasn't been chosen"
            )
        serv.active_editor.show()

    def _on_generate_visualization_clicked(self):
        serv = self._service
        if not serv:
            raise InvalidInteractionError(
                "Attempted to generate visualization without anything to visualize"
            )

        location = self._save_path
        serv.save_visualization(location)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(location)))
