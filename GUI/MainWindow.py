import os
import sys

from PyQt6 import QtCore
from PyQt6.QtCore import QEvent, QRect
from PyQt6.QtWidgets import QSizePolicy, QApplication, QMainWindow, QVBoxLayout, \
    QFileDialog, QStackedLayout, QTabWidget
from PyQt6.QtWidgets import QWidget

from DBService.DBUIAdapter import DBUIAdapter
from GUI.CliInOutWorkerThreadManager import CliInOutWorkerThreadManager
from GUI.Custom.CustomDataTable import CustomDataTable
from GUI.Custom.CustomDragDropWidget import DragDropWidget
from GUI.Custom.CustomTitleBar import CustomTitleBar
from GUI.Custom.CustomLiveWidget import CustomLiveWidget
from GUI.Custom.DummyDataGenerator import DummyDataGenerator
from GUI.Custom.CustomDialog import ContentType, CustomDialog
from GUI.LeftNavigation import LeftNavigation
from GUI.Menu.DisplayPlasmidTubes import DisplayPlasmidTubes
from GUI.Menu.DisplayQRCode import DisplayQRCode
from GUI.Menu.ExperimentPreparation import ExperimentPreparation
from GUI.Menu.ExperimentPreparationWidget import ExperimentPreparationWidget
from GUI.Menu.HomePageDashboard import HomePageDashboard
from GUI.Menu.QRCodesWidget import QRCodesWidget
from GUI.Menu.Settings import Settings
from GUI.Menu.TableInformationFetchByParameter import TableInformationFetchByParameter
from GUI.Navigation import Ui_MainWindow
from GUI.ResizeGripWidget import ResizeGripWidget

__author__ = 'Ujwal Subedi'
__date__ = '01/12/2023'
__version__ = '1.0'
__last_changed__ = '01/12/2023'

from GUI.Storage.BorgSingleton import TubesSingleton, CurrentExperimentSingleton
from GUI.Menu.experiment_tubes_info_view import ExperimentTubesInfoDashboard, ExperimentTubesDetails
from GUI.Storage.Cache import Cache
from GUI.Storage.CacheModel import CacheModel


class MainWindow(QMainWindow):
    """
    This is the Main Window for all the Graphical User Interface to Work and bind together. Most of the Initializations are stated here.
    """

    def __init__(self):
        super(MainWindow, self).__init__()

        # UI Mainwindow Configuration
        self.tab_widget_experiment_qr = None
        self.home_dashboard = None
        self.tab_widget_home_dashboard = None
        self.cache = Cache("application_cache.json")
        try:
            self.cache_data = self.load_cache()
            if self.cache_data:
                if self.cache_data.experiment_id:
                    self.current_experiment = CurrentExperimentSingleton(self.cache_data.experiment_id)
        except Exception as ex:
            print(ex)
            self.cache_data = None

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.homePage.hide()

        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.home_btn_dashboard.setChecked(True)
        self.setWindowTitle("Dashboard GUI")
        self.resizeGrip = ResizeGripWidget(self)
        self.resizeGrip.setGeometry(self.width() - 16, self.height() - 16, 16, 16)
        self.resizeGrip.show()
        self.apply_stylesheet()

        # self.setGeometry(100, 100, 800, 600)
        self.process = any

        # Database Service Connection Adapter
        self.ui_db = DBUIAdapter()

        # Custom Titlebar
        self.title_bar = CustomTitleBar(self)
        self.setMenuWidget(self.title_bar)
        self.setWindowTitle("Dashboard UI")

        # TODO delete later
        self.ui.experimentImportierenVorbereitung.hide()

        # Save all the contents of the dialog box, before adding anything , it is better idea to remove contents
        # which are saved here
        self.dialogBoxContents = []

        # drag & drop import concept
        self.ui.importAreaDragDrop.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint, True)
        self.ui.importAreaDragDrop = DragDropWidget(self.ui.importPage, self.ui_db)
        self.ui.importAreaDragDrop.setObjectName(u"dragdropwidget")
        self.ui.importAreaDragDrop.setGeometry(QRect(130, 90, 461, 261))
        self.ui.importAreaDragDrop.setStyleSheet(u"background-color:#666;")
        self.ui.chooseFileFromExplorer.clicked.connect(self.openFileDialog)

        # Custom ModalDialogBox
        self.dialog = CustomDialog(self)
        self.dialog.sendButtonClicked.connect(self.send_button_dialog_clicked)
        # self.dialogBox.hideDialog()

        # Experiment Table with Tubes view
        self.setupExperimentView()
        # home dashboard
        # self.home_dashboard = HomePageDashboard(self.ui.test_page_home, self)
        self.setupHomeDashboardView()

        # ExperimentPreparation Pages
        self.experiment_preparation = ExperimentPreparation(self.ui, self)
        self.experiment_preparation.map_prev_next(self.ui)

        left_navigation = LeftNavigation(self.ui)
        left_navigation.map_buttons_to_pages()

        self.ui.generateQrBtn.clicked.connect(self.add_qr_generation_info)

        self.ui.startEnTBtn.clicked.connect(self.startEnTProcess)

        # Live view widget
        widget_live_layout = QVBoxLayout(self.ui.widgetLive)
        self.custom_live_widget = CustomLiveWidget(self.ui.widgetLive)
        widget_live_layout.addWidget(self.custom_live_widget)

        # Cli stdin stdout
        self.cliInOutWorkerThreadManager = CliInOutWorkerThreadManager(self.ui)
        self.ui.sendBtnInputFromCli.clicked.connect(self.cliInOutWorkerThreadManager.send_input)

        # Experiment Data
        experiment_table_layout = QVBoxLayout()
        generator = DummyDataGenerator()
        generator.generate_random_entries_experiment(15)
        df_exp = generator.to_dataframe_experiment()
        experiment_data_table = CustomDataTable(df_exp, self.ui.experimentView)
        experiment_table_layout.addWidget(experiment_data_table)
        self.ui.experimentView.setLayout(experiment_table_layout)

        plasmid_table_layout = QVBoxLayout()
        generator.generate_random_entries_plasmid(15)
        df_exp = generator.to_dataframe_plasmid()
        plasmid_table = CustomDataTable(df_exp, self.ui.plasmidMetadatenView)
        plasmid_table_layout.addWidget(plasmid_table)
        self.ui.plasmidMetadatenView.setLayout(plasmid_table_layout)

        # settings
        self.settings = Settings(self.ui, self)
        self.ui.windowResizeSlider.valueChanged.connect(self.settings.resize_window)

        # Display Plasmid Tubes
        self.plasmidTubesList = DisplayPlasmidTubes(self.ui, self)

        self.ui.experimentImportierenVorbereitung.clicked.connect(lambda: self.openFileDialog('experiment'))
        self.ui.importPlasmidMetadaten.clicked.connect(lambda: self.openFileDialog('plasmid'))
        self.ui.plasmidMetaDataImport.clicked.connect(lambda: self.openFileDialog('plasmid'))

        # Display TubeInformation
        self.tube_info = TableInformationFetchByParameter(self.ui, self)
        self.ui.tube_info_load_btn.clicked.connect(self.tube_info.load_and_display_tube_info)

        # reorganise layout

        # self.ui.vorbereitungStackedTab.setParent(self.ui.statistikPage)

    def save_cache(self, arg, value):
        arg = "user_preferences"
        value = {"experiment_id": value, "language": "en"}
        self.cache.save({f"{arg}": value})

    def load_cache(self):
        try:
            preferences = self.cache.load()
            if preferences:
                # Assuming preferences is a dictionary with the key "user_preferences"
                user_prefs = preferences.get("user_preferences", {})
                cache_data = CacheModel(experiment_id=user_prefs.get("experiment_id"),
                                        language=user_prefs.get("language"))
                print(cache_data)
                return cache_data
        except Exception as ex:
            print(ex)
        return None

    def setupHomeDashboardView(self):
        try:
            # Create a QVBoxLayout for the main layout
            main_layout = QVBoxLayout(self.ui.test_page_home)

            # Create the QTabWidget for the tabs
            self.tab_widget_home_dashboard = QTabWidget(self.ui.test_page_home)

            # Add HomePageDashboard to the layout
            self.home_dashboard = HomePageDashboard(self.ui.test_page_home, self)
            # self.home_dashboard.show_start_button()
            self.tab_widget_home_dashboard.addTab(self.home_dashboard, "Dashboard")
            # Add CustomLiveWidget to the layout
            # live_widget = CustomLiveWidget(self.ui.test_page_home)
            # self.tab_widget_home_dashboard.addTab(live_widget, "Live")
            # ExperimentPreparation Pages

            # experiment_preparation.map_prev_next(self.ui)
            # self.tab_widget_home_dashboard.addTab(experiment_preparation, "Exp Vorb")
            # vorbereitung_index = self.tab_widget_home_dashboard.indexOf(self)
            # self.tab_widget_home_dashboard.setCurrentIndex(vorbereitung_index)

            # Add the tab widget to the main layout
            main_layout.addWidget(self.tab_widget_home_dashboard)

        except Exception as ex:
            print(ex)

    def setupExperimentView(self):
        try:
            # Create a QVBoxLayout for the main layout
            main_layout = QVBoxLayout(self.ui.experiment_info_view)

            # Create the QTabWidget for the tabs
            self.tab_widget_experiment_qr = QTabWidget(self.ui.experiment_info_view)

            # Create the content for the first tab (Experiment Tubes)
            experiment_tubes_widget = QWidget()  # Container widget for the first tab
            experiment_tubes_layout = QVBoxLayout(experiment_tubes_widget)  # Layout for the container widget

            # Add your existing stacked layout to the first tab
            stacked_layout = QStackedLayout()

            dashboard = ExperimentTubesInfoDashboard(parent=self.ui.experiment_info_view, main_window=self)
            details = ExperimentTubesDetails(main_window=self)

            stacked_layout.addWidget(dashboard)
            stacked_layout.addWidget(details)

            # Connect signals as before
            dashboard.experiment_selected.connect(
                lambda data: self.show_experiment_details(data, details, stacked_layout))
            details.back_to_dashboard.connect(lambda: stacked_layout.setCurrentIndex(0))

            experiment_tubes_layout.addLayout(stacked_layout)
            self.tab_widget_experiment_qr.addTab(experiment_tubes_widget, "Experiment Tubes")

            # Creates and adds tab for QR Codes
            qr_codes_widget = QRCodesWidget(self.ui.experiment_info_view, self)
            self.tab_widget_experiment_qr.addTab(qr_codes_widget, "QR Codes")
            # Load data to the Row
            qr_codes_widget.refresh_data()

            # Add the tab widget to the main layout
            main_layout.addWidget(self.tab_widget_experiment_qr)

        except Exception as ex:
            print(ex)

    def show_experiment_details(self, data, details_widget, stacked_layout):
        details_widget.update_details(data)
        stacked_layout.setCurrentIndex(1)

    def display_qr_from_main(self, qr_code_list):
        tube_information = TubesSingleton()
        print("----Main----")
        qr_code_display = DisplayQRCode(self.ui, self)
        for tube in qr_code_list:
            # print(tube_information.tubes[tube].qr_code)
            qr_code_display.displayQrCode(tube)
        # Display QR Codes

    def show_message_in_dialog(self, display_msg):
        self.dialogBoxContents.append(
            self.dialog.addContent(f"{display_msg}", ContentType.OUTPUT))
        self.dialog.show()

    def set_expanding_size_policy(self, widget):
        """
        Set the size policy of all child widgets of 'widget' to Expanding.
        """
        for child in widget.findChildren(QWidget):
            child.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def removeDialogBoxContents(self):
        """
        Removes all the Contents of the Dialog Box. It is better to call this method before showing new contents in the Box.
        """
        if self.dialogBoxContents.count:
            self.dialog.removeItems(self.dialogBoxContents)

    def openFileDialog(self, file_type):
        """
        Shows a Window File Selector UI Widget to select an Excel File to be imported.
        """
        file_name, _ = QFileDialog.getOpenFileName(self.ui.centralwidget, "Open File", "", "Excel Files (*.xls *.xlsx)")
        if file_name:
            print(f'Selected file: {file_name}')
            try:
                # df = pd.read_excel(file_name)
                # TODO show message in dialogbox
                self.removeDialogBoxContents()

                if file_type == 'experiment':
                    message = self.ui_db.insert_experiment_data(file_name)
                elif file_type == 'plasmid':
                    message = self.ui_db.insert_metadaten(file_name)
                if message is not None:
                    display_msg = " ".join(str(item) for item in message)
                else:
                    display_msg = "No Display Text"
                self.dialogBoxContents.append(self.dialog.addContent(f"{display_msg}", ContentType.OUTPUT))

            except Exception as e:
                print(f'Error occurred while importing Excel file: {file_name}\n{str(e)}')
                self.dialogBoxContents.append(
                    self.dialog.addContent(f"Error occurred while importing Excel file: {file_name}",
                                           ContentType.OUTPUT))
                self.dialogBoxContents.append(self.dialog.addContent(f" {str(e)}", ContentType.OUTPUT))
            finally:
                print(f'Successfully imported Excel file: {file_name}')
                self.dialogBoxContents.append(
                    self.dialog.addContent(f'Successfully imported Excel file: {file_name}', ContentType.OUTPUT))
            self.dialog.show()

    def eventFilter(self, source, event):
        if source == self.ui.tableWidgetLiveAction and event.type() == QEvent.Type.Resize:
            self.arrow_overlay.setGeometry(self.ui.tableWidgetLiveAction.geometry())
        return super().eventFilter(source, event)

    def startEnTProcess(self):
        """
        Start the Monitoring App, change button color on the current situation of the Process.
        """
        # TODO Start monitoring app using python process

        if self.ui.startEnTBtn.text() == "Start":
            self.ui.startEnTBtn.setStyleSheet("QPushButton { background-color: red }")
            self.ui.startEnTBtn.setText("Stop")
            self.cliInOutWorkerThreadManager.displayDefault("Process has been started.")
            self.cliInOutWorkerThreadManager.startProcess()

        else:
            self.ui.startEnTBtn.setStyleSheet("QPushButton { background-color: #45a049 }")
            self.cliInOutWorkerThreadManager.stopProcess()
            self.cliInOutWorkerThreadManager.displayDefault("Process has been stopped.")
            print("E&T process Terminated!")
            self.ui.startEnTBtn.setText("Start")

    def handle_message(self, message):
        # TODO show this message in display box
        print(message + " recieved from client")
        message_split = message.split()
        if message_split[0] == "INPUT":
            if self.dialogBoxContents:
                print(self.dialogBoxContents)
                self.dialog.removeItems(self.dialogBoxContents)
            self.dialogBoxContents.append(
                self.dialog.addContent(f"Bitte {message_split[1]} eingeben: ", ContentType.INPUT))

            if not self.dialog.isVisible():
                self.dialog.show()

    def send_button_dialog_clicked(self):
        text = self.dialog.lineEditTextChanged
        self.worker_thread.send_message("ANZAHL_TUBES " + text)
        if self.dialogBoxContents:
            self.dialog.removeItems(self.dialogBoxContents)
        self.dialogBoxContents.append(
            self.dialog.addContent(f"Erfassung & Tracking gestartet mit {text} Tubes. \n ", ContentType.OUTPUT))
        return text

    def importPlasmidMetaDaten(self):
        fileName, _ = QFileDialog.getOpenFileName(self.ui.centralwidget, "Open File", "", "Excel Files (*.xls *.xlsx)")
        if fileName:
            print(f'Selected file: {fileName}')
            try:
                # df = pd.read_excel(fileName)
                # TODO show message in dialogbox
                if self.dialogBoxContents.count:
                    self.dialog.removeItems(self.dialogBoxContents)
                print(f'Successfully imported Excel file: {fileName}')
                self.dialogBoxContents.append(
                    self.dialog.addContent(f'Successfully imported Excel file: {fileName}', ContentType.OUTPUT))
                message = self.ui_db.insert_metadaten(fileName)
                if message is not None:
                    displayMsg = " ".join(str(item) for item in message)
                else:
                    displayMsg = "No Display Text"
                self.dialogBoxContents.append(self.dialog.addContent(f"{displayMsg}", ContentType.OUTPUT))

            except Exception as e:
                print(f'Error occurred while importing Excel file: {fileName}\n{str(e)}')
                self.dialogBoxContents.append(
                    self.dialog.addContent(f"Error occurred while importing Excel file: {fileName}",
                                           ContentType.OUTPUT))
                self.dialogBoxContents.append(self.dialog.addContent(f" {str(e)}", ContentType.OUTPUT))

    def apply_stylesheet(self):
        """
        Load Stylesheet from the file and implement it to the UI.
        """
        print(os.getcwd())
        if os.path.isfile('GUI/stylesheet/stylen.qss') and os.access('GUI/stylesheet/stylen.qss', os.R_OK):
            print("File exists and is readable")
            with open('GUI/stylesheet/stylen.qss', 'r') as file:
                stylesheet = file.read()
            self.setStyleSheet(stylesheet)
        else:
            print("Stylesheet File is either missing or not readable")

    def add_qr_generation_info(self):
        nrOfQr = self.ui.qrNrInputBox.text()
        data = self.ui_db.create_qr_code(int(nrOfQr))
        if data:
            qr_code_generated = "Folgende QR Codes sind generiert: \n" + "\n".join(
                [f"{qr_code.qr_code} - {qr_code.datum}" for qr_code in data])
            self.ui.infoBoxQr.setText(qr_code_generated)
        else:
            self.ui.infoBoxQr.setText("No QR codes were generated.")
        self.ui.qrNrInputBox.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
