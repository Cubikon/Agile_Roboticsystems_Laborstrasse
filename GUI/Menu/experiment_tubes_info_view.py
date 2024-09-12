from PyQt6.QtCore import pyqtSignal, Qt, QSize, QTimer
from PyQt6.QtGui import QColor, QPalette, QIcon, QPixmap, QCursor
from PyQt6.QtWidgets import (QWidget, QPushButton, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem,
                             QAbstractItemView, QHeaderView, QApplication, QMessageBox, QSystemTrayIcon, QToolTip,
                             QHBoxLayout)
from PyQt6.uic.properties import QtGui

from GUI.Storage.BorgSingleton import ExperimentSingleton, CurrentExperimentSingleton
from GUI.button_back_design_test import CustomBackButton


class ExperimentTubesDetails(QWidget):
    """
    Load Experiment Details after clicking on the table item.
    """
    back_to_dashboard = pyqtSignal()  # Signal to indicate when to go back to the dashboard

    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.back_button = None
        self.details_table = None
        self.title = None
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        # Back button.
        icon_pixmap = QPixmap(":/icons/img/arrow-left.svg").scaled(
            200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
        )
        self.back_button = CustomBackButton('Zurück', icon_pixmap, self)
        self.back_button.setStyleSheet("background:#FF0000;")
        self.back_button.setGeometry(50, 20, 100, 50)
        self.back_button.clicked.connect(self.on_back_clicked)

        # layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignLeft)

        layout = QVBoxLayout(self)
        self.title = QLabel('Experiment Details')
        layout.addWidget(self.title)
        layout.addStretch(1)

        # Initialize the details table
        self.details_table = self.initialize_details_table()
        layout.addWidget(self.details_table)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def initialize_details_table(self):
        details_table = QTableWidget(10, 2)  # 10 rows, 2 columns
        details_table.setHorizontalHeaderLabels(['Field', 'Value'])
        details_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        details_table.cellDoubleClicked.connect(self.copy_to_clipboard)
        return details_table

    def copy_to_clipboard(self, row, column):
        item = self.details_table.item(row, column)
        if item is not None:
            try:
                QApplication.clipboard().setText(item.text())
                QToolTip.showText(QCursor.pos(), "Copied")
                QTimer.singleShot(5000, QToolTip.hideText)
            except Exception as ex:
                print(ex)

    def update_details(self, experiment_data):
        try:
            # Update the title
            self.title.setText(f"Experiment ID: {experiment_data['probe_nr']}")

            # Reset the table rows
            self.details_table.setRowCount(10)
            self.main_window.title_bar.add_back_btn(self.back_button)

            # Populate the table with the data
            fields = ['Probe Nr', 'QR Code', 'Plasmid Nr', 'Vektor', 'Insert', 'Name', 'Vorname', 'Exp ID', 'Datum',
                      'Anz Fehler']
            for i, field in enumerate(fields):
                value = str(experiment_data[field.lower().replace(' ', '_')])

                item_field = QTableWidgetItem(field)
                item_field.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.details_table.setItem(i, 0, item_field)

                item_value = QTableWidgetItem(value)
                item_value.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.details_table.setItem(i, 1, item_value)

            header = self.details_table.horizontalHeader()

            # Set the left column to resize to contents
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)

            # Set the right column to stretch to fill the table width
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

            # Add the table to the layout
            self.layout().addWidget(self.details_table)
        except Exception as ex:
            print(ex)

    def on_back_clicked(self):
        self.back_button.setParent(None)
        self.back_to_dashboard.emit()


class ExperimentTubesInfoDashboard(QWidget):
    experiment_selected = pyqtSignal(dict)  # Signal to indicate an experiment is selected

    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window
        self.ui_db = self.main_window.ui_db

        if main_window.cache_data:
            self.experiments_data = self.ui_db.experiment_adapter.get_tubes_data_for_experiment(
                main_window.cache_data.experiment_id)
        else:
            self.experiments_data = None
        self.experiments_table = None
        self.db_ui = None

        self.initUI()

    def initUI(self):

        layout = QVBoxLayout(self)
        # Header area
        h_layout = QHBoxLayout()
        header_label = QLabel('Experiments Overview')
        h_layout.addWidget(header_label)

        h_layout.addStretch(1)  # This will push the following widgets to the right

        self.create_refresh_btn(h_layout)

        layout.addLayout(h_layout)
        self.setLayout(layout)
        self.current_experiment = CurrentExperimentSingleton()

        row = 0 if self.experiments_data is None else len(self.experiments_data)

        # Creates the experiments table
        self.experiments_table = QTableWidget(row, 10)
        self.experiments_table.setHorizontalHeaderLabels(
            ['Probe Nr', 'QR Code', 'Plasmid Nr', 'Vektor', 'Insert', 'Name', 'Vorname', 'Exp ID', 'Datum',
             'Anz Fehler'])

        header = self.experiments_table.horizontalHeader()

        # Set all columns to stretch to fill the table width
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Set the last column to resize to contents
        header.setSectionResizeMode(9, QHeaderView.ResizeMode.ResizeToContents)

        self.populate_table()

        layout.addWidget(self.experiments_table)

        # Set the selection behavior to select the entire row
        self.experiments_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.experiments_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.experiments_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # Change the hover color
        hover_palette = self.experiments_table.palette()
        hover_palette.setColor(QPalette.ColorRole.Highlight, QColor(200, 200, 200))
        self.experiments_table.setPalette(hover_palette)

        # Connect the cell click signal
        self.experiments_table.cellClicked.connect(self.row_selected)

    def create_refresh_btn(self, h_layout):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/img/refresh-double.svg"), QIcon.Mode.Normal,
                       QIcon.State.Off)
        refresh_btn = QPushButton("")
        refresh_btn.clicked.connect(self.refresh_data)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
            }
            QPushButton:hover {
                background: #eee;
            }
        """)
        refresh_btn.setToolTip("Refresh")
        refresh_btn.setIcon(icon)
        h_layout.addWidget(refresh_btn)

    def refresh_data(self):
        try:
            self.main_window.cache_data = self.main_window.load_cache()
            if self.main_window.cache_data or (hasattr(CurrentExperimentSingleton,
                                                       'experiment_id') and self.current_experiment.experiment_id is not None):
                self.current_experiment.experiment_id = self.main_window.cache_data.experiment_id
                self.experiments_data = self.ui_db.experiment_adapter.get_tubes_data_for_experiment(self.current_experiment.experiment_id)
                self.populate_table()
            else:
                self.current_experiment = self.main_window.cache_data.experiment_id
        except Exception as ex:
            self.main_window.removeDialogBoxContents()
            self.main_window.show_message_in_dialog(ex)

    def populate_table(self):
        try:
            if self.experiments_data:
                self.experiments_table.setRowCount(0)
                for i, experiment in enumerate(self.experiments_data):
                    self.experiments_table.insertRow(i)
                    self.experiments_table.setItem(i, 0, QTableWidgetItem(str(experiment['probe_nr'])))
                    self.experiments_table.setItem(i, 1, QTableWidgetItem(experiment['qr_code']))
                    self.experiments_table.setItem(i, 2, QTableWidgetItem(experiment['plasmid_nr']))
                    self.experiments_table.setItem(i, 3, QTableWidgetItem(experiment['vektor']))
                    self.experiments_table.setItem(i, 4, QTableWidgetItem(experiment['insert']))
                    self.experiments_table.setItem(i, 5, QTableWidgetItem(experiment['name']))
                    self.experiments_table.setItem(i, 6, QTableWidgetItem(experiment['vorname']))
                    self.experiments_table.setItem(i, 7, QTableWidgetItem(experiment['exp_id']))
                    self.experiments_table.setItem(i, 8, QTableWidgetItem(experiment['datum']))
                    self.experiments_table.setItem(i, 9, QTableWidgetItem(str(experiment['anz_fehler'])))
            else:
                # Check if the table is empty
                if self.experiments_table.rowCount() == 0:
                    self.main_window.removeDialogBoxContents()
                    self.main_window.show_message_in_dialog("Empty Table, No Data!")
        except Exception as ex:
            print(ex)
            print(ex.with_traceback())

    def row_selected(self, row, column):
        experiment_data = self.experiments_data[row]
        self.experiment_selected.emit(experiment_data)
