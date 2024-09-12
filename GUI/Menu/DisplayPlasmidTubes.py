import os
import qrcode

from GUI.Custom.CustomDialog import ContentType
from GUI.Navigation import Ui_MainWindow
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QProcess
from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QApplication, QSizePolicy, QScrollArea, QFrame
from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QLabel, QLineEdit
from PyQt6.QtCore import Qt
from GUI.Navigation import Ui_MainWindow
from PyQt6 import sip

__author__ = 'Ujwal Subedi'
__date__ = '01/12/2023'
__version__ = '1.0'
__last_changed__ = '01/12/2023'

from GUI.Storage.BorgSingleton import ExperimentSingleton


class DisplayPlasmidTubes(QWidget):
    """
    Shows the List of Plasmid and an Input field which accepts Probe Nr as a List in comma Separated Values like 5,6,9.
    """

    def __init__(self, ui: Ui_MainWindow, main_window):
        super().__init__()
        self.ui = ui
        self.main_window = main_window

        scroll = QScrollArea(self)
        self.ui.plasmidProbeList.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Disable horizontal scrolling

        frame = QFrame(scroll)
        scroll.setWidget(frame)
        self.outputLayout = QVBoxLayout(frame)
        self.experiment_data = ExperimentSingleton()
        self.plasmid_tubes = {}
        self.tubes_input_fields = []

    def displayPlasmidTubes(self, plasmid_nr_list, plasmid_dict):

        for i in reversed(range(self.outputLayout.count())):
            widget = self.outputLayout.itemAt(i).widget().setParent(None)
            if widget is not None:
                widget.setParent(None)
                sip.delete(widget)

        print(self.experiment_data)
        starting_info_txt = QLabel(
            f"Experiment Id: {self.experiment_data.experiment_id} | {self.experiment_data.firstname}, {self.experiment_data.lastname}")
        text_widget = QWidget()  # Create a QWidget
        text_layout = QHBoxLayout()  # Create a QHBoxLayout
        text_layout.addWidget(starting_info_txt)  # Add your QLabel to the QHBoxLayout
        text_widget.setLayout(text_layout)  # Set the layout of the QWidget to your QHBoxLayout
        self.outputLayout.addWidget(text_widget)  # Add the QWidget to your outputLayout

        for elem in plasmid_nr_list:
            # add list here
            self.appendOutput(elem)

    def appendOutput(self, plasmid_nr):
        widget = QWidget()
        widget.setObjectName("displayPlasmidTubes")
        self.outputLayout.addWidget(widget)
        # Create the buttons and line edit
        plasmid_nr_label = QLabel(plasmid_nr)
        probe_nr_input = QLineEdit()
        self.tubes_input_fields.append(probe_nr_input)
        print(plasmid_nr)
        probe_nr_input.editingFinished.connect(
            lambda: self.save_tubes_to_plasmid(probe_nr_input.text(), plasmid_nr))

        probe_nr_input.setPlaceholderText("Probe Nr eingeben. Bsp : 1,3,4,7")
        # probe_nr_input.setFixedWidth(120)
        h_layout = QHBoxLayout(widget)

        # Create a QWidget and set the QVBoxLayout on it
        v_widget = QWidget()
        # Add the QWidget to the QHBoxLayout
        h_layout.addWidget(v_widget)
        h_layout.addWidget(plasmid_nr_label)
        h_layout.addWidget(probe_nr_input)

    def save_tubes_to_plasmid(self, text, plasmid_nr):
        # add tubes in the borg list for each plasmid
        print("input probe")
        print(text)
        print(plasmid_nr)
        try:
            self.experiment_data.plasmid_tubes[plasmid_nr] = [int(num) for num in text.split(',')]
            print(self.experiment_data.plasmid_tubes)
        except Exception as ex:
            self.main_window.dialogBoxContents.append(
                self.main_window.dialog.addContent(f"Please check the Input. \n{ex}", ContentType.OUTPUT))
            self.main_window.dialog.show()

    def check_duplicate_inputs(self):
        input_values = []
        for field in self.tubes_input_fields:
            input_values.extend(field.text().split(','))

        if len(input_values) != len(set(input_values)):
            print("Duplicate inputs found.")
            return True
        else:
            print("No duplicate inputs.")
            return False

    def check_max_input(self):
        input_values = []
        for field in self.tubes_input_fields:
            input_values.extend(field.text().split(','))

        if len(input_values)>32:
            return False

        return True

