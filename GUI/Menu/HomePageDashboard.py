from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy

from GUI.Menu.ExperimentPreparationWidget import ExperimentPreparationWidget


class HomePageDashboard(QWidget):
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.startEnTBtn = None
        self.main_window = main_window
        self.ui = main_window.ui
        # Set size policy to expanding
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Create a QVBoxLayout
        self.vbox_layout = QVBoxLayout(self)
        self.show_experiment_preparation()
        # self.show_start_button()
        self.show_start_button_details()

    def create_refresh_btn(self):
        return QPushButton("Refresh")

    def show_experiment_preparation(self):
        # Create a horizontal layout for buttons
        hbox_layout = QHBoxLayout()

        # Create buttons and add them to the horizontal layout
        start_label = QLabel("Experiment Vorbereitung")
        hbox_layout.addWidget(start_label)

        # Add a stretch to push the next widget (button2) to the right
        hbox_layout.addStretch()

        start = QPushButton("Start")
        start.setMinimumSize(200, 240)
        start.clicked.connect(self.start_experiment_preparation)
        hbox_layout.addWidget(start)

        # Add the horizontal layout to the vertical layout
        self.vbox_layout.addLayout(hbox_layout)

    def show_start_button(self):
        # Create a horizontal layout for buttons
        hbox_layout = QHBoxLayout()

        # Create label and add it to the horizontal layout
        start_label = QLabel("Start Erfassung & Tracking")
        hbox_layout.addWidget(start_label)

        # Add a stretch to push the next widget (button) to the right
        hbox_layout.addStretch()

        # Create the start button and add it to the layout
        self.startEnTBtn = QPushButton("Start")
        self.startEnTBtn.setMinimumSize(200, 240)
        self.startEnTBtn.clicked.connect(self.startEnTProcess)
        hbox_layout.addWidget(self.startEnTBtn)

        # Add the horizontal layout to the vertical layout
        self.vbox_layout.addLayout(hbox_layout)

    def show_start_button_details(self):
        # Create a widget and set its object name
        widget = QWidget()

        # Create a horizontal layout for the widget
        h_layout = QHBoxLayout(widget)

        # Create a label for the probe number
        probe_nr_text = QLabel("")
        probe_nr_text.setFixedWidth(120)

        # Create the buttons
        drucken = QPushButton("Drucken")
        speichern = QPushButton("Speichern")
        h_layout.addWidget(probe_nr_text)

        # Add a stretch to push the buttons to the right
        h_layout.addStretch()

        # h_layout.addWidget(speichern)
        # h_layout.addWidget(drucken)

        # Add the widget to your main QVBoxLayout
        self.vbox_layout.addWidget(widget)

    def add_other_page_nav_btns(self):
        # Create a widget and set its object name
        widget = QWidget()

        # Create a horizontal layout for the widget
        h_layout = QHBoxLayout(widget)

        # Create a label for the probe number
        probe_nr_text = QLabel("Navigate to other Pages")
        probe_nr_text.setFixedWidth(120)
        h_layout.addWidget(probe_nr_text)

        # Create the buttons
        live_view = QPushButton("Live View")
        show_qr = QPushButton("Show QR Codes")
        all_tubes_exp = QPushButton("All Tubes of current Experiment")

        # map buttons
        live_view.clicked.connect(lambda: (
            self.ui.home_btn_dashboard.setChecked(True), self.main_window.tab_widget_home_dashboard.setCurrentIndex(1)))
        show_qr.clicked.connect(lambda: (
            self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.experiment_info_view)),
            self.main_window.tab_widget_experiment_qr.setCurrentIndex(1)))
        all_tubes_exp.clicked.connect(lambda: (
            self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.experiment_info_view)),
            self.main_window.tab_widget_experiment_qr.setCurrentIndex(0)))

        # Add a stretch to push the buttons to the right
        h_layout.addStretch()

        h_layout.addWidget(live_view)
        h_layout.addWidget(show_qr)
        h_layout.addWidget(all_tubes_exp)

        # Add the widget to your main QVBoxLayout
        self.vbox_layout.addWidget(widget)

    def startEnTProcess(self):
        """
        Start the Monitoring App, change button color on the current situation of the Process.
        """
        # TODO Start monitoring app using python process

        if self.startEnTBtn.text() == "Start":
            self.startEnTBtn.setStyleSheet("QPushButton { background-color: red }")
            self.startEnTBtn.setText("Stop")
            self.main_window.cliInOutWorkerThreadManager.displayDefault("Process has been started.")
            self.main_window.cliInOutWorkerThreadManager.startProcess()

        else:
            self.startEnTBtn.setStyleSheet("QPushButton { background-color: #45a049 }")
            self.main_window.cliInOutWorkerThreadManager.stopProcess()
            self.main_window.cliInOutWorkerThreadManager.displayDefault("Process has been stopped.")
            print("E&T process Terminated!")
            self.startEnTBtn.setText("Start")

    def start_experiment_preparation(self):
        # TODO - after loading vorbereitung page- after finished creating tubes and experiment hide the experiment prep
        #  page and show the dashboard page with start ent app.
        #  below it show buttons to show qr codes and load experiment tubes table pages
        experiment_preparation = ExperimentPreparationWidget(self.ui.vorbereitungStackedTab, self.ui.test_page_home)
        experiment_preparation.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        experiment_preparation.addToMainWindow(self.main_window)
        # hide other tabs
        # self.main_window.tab_widget_home_dashboard.removeTab(1)
        # self.main_window.tab_widget_home_dashboard.removeTab(2)
