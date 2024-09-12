from DBService.DBUIAdapter import DBUIAdapter
from GUI.Custom.CustomDialog import ContentType, CustomDialog
from GUI.Custom.CustomLiveWidget import CustomLiveWidget
from GUI.Menu.DisplayQRCode import DisplayQRCode
from GUI.Menu.ExperimentPreparationWidget import ExperimentPreparationWidget
from GUI.Navigation import Ui_MainWindow
from PyQt6.QtCore import pyqtSignal, QDate
import datetime

__author__ = 'Ujwal Subedi'
__date__ = '01/12/2023'
__version__ = '1.0'
__last_changed__ = '03/12/2023'

from GUI.Storage.BorgSingleton import ExperimentSingleton, TubesSingleton, CurrentExperimentSingleton


class ExperimentPreparation:
    """
    Experiment Preparation window functionalities.
    """
    sendButtonClicked = pyqtSignal(str)

    def __init__(self, ui: Ui_MainWindow, main_window):
        self.tube_information = TubesSingleton()
        self.experiment_data = ExperimentSingleton()
        self.ui = ui
        self.main_window = main_window
        self.qr_code_display = DisplayQRCode(self.ui, self.main_window)
        self.ui.experimentIdLE.editingFinished.connect(lambda: self.checkExperimentID(self.ui.experimentIdLE.text()))
        self.ui.nameLE.editingFinished.connect(lambda: self.create_experiment_id(self.ui.nameLE.text()))
        self.dialog = CustomDialog(self.ui.centralwidget)
        self.ui_database = main_window.ui_db
        self.qr_code_generator = DisplayQRCode(self.ui, self.main_window)
        self.current_experiment = None

        # Set the datumLE to current Date
        today = datetime.datetime.today()
        qdate = QDate(today.year, today.month, today.day)
        self.ui.datumLE.setDate(qdate)

    def create_experiment_id(self, text):
        try:
            exp_id_data = self.ui_database.adapter.get_experiment_by_id(text)
            print(exp_id_data)
        except Exception as ex:
            print(ex)

    def checkExperimentID(self, text):
        # TODO: check in db
        try:
            exp_id_data = self.ui_database.adapter.get_experiment_by_id(text)
            plasmids = self.ui_database.get_plasmids_for_experiment(self.experiment_data.experiment_id)
            if exp_id_data:
                self.ui.nameLE.setText(exp_id_data.name)
                self.ui.vornameLE.setText(exp_id_data.vorname)
                self.ui.anzahlTubesLE.setText(str(exp_id_data.anz_tubes))
                self.ui.anzahlPlasmidLE.setText(str(exp_id_data.anz_plasmid))
                # Convert a date string to a datetime.date object
                date = datetime.datetime.strptime(exp_id_data.datum, '%Y-%m-%d').date()
                # Convert a datetime.date to QDate
                qdate = QDate(date.year, date.month, date.day)
                # Set the date of the QDateEdit widget
                self.ui.datumLE.setDate(qdate)
                print(exp_id_data)
                if plasmids:
                    plasmid_list = list(set(plasmids))
                    plasmid_string = ','.join(plasmid_list)
                    self.ui.plasmidListEV_LE.setText(plasmid_string)

        except Exception as ex:
            print(ex)

    def nextPage(self):
        current_index = self.ui.vorbereitungStackedTab.currentIndex()
        if current_index < self.ui.vorbereitungStackedTab.count() - 1:
            self.ui.vorbereitungStackedTab.setCurrentIndex(current_index + 1)

    def nextPageWithControl(self, page_data):
        if page_data == 'CreateExperiment':
            # TODO: verify if plasmid exists
            print("weiter clicked " + page_data)
            # self.main_window.plasmidTubesList.displayPlasmidTubes("test")
            # self.nextPage()
            try:
                self.experiment_creation(page_data)
            except Exception as ex:
                display_msg = "Could not create Experiment.\n"
                self.main_window.dialogBoxContents.append(
                    self.main_window.dialog.addContent(f"{display_msg} {ex}", ContentType.OUTPUT))
                self.main_window.dialog.show()

        elif page_data == 'AddProbeToPlasmid':
            # TODO: add data to tubes table
            print("AddProbeToPlasmid")
            self.tube_information.clear_cache()
            self.main_window.removeDialogBoxContents()

            # self.nextPage()
            if self.check_duplicates(self.experiment_data.plasmid_tubes):
                display_msg = "Experiment has duplicates, please re-enter!"
                self.show_message_in_dialog(display_msg)

            # # TODO check this before inserting data
            # elif not self.main_window.plasmidTubesList.check_duplicate_inputs():
            #     self.main_window.display_qr_from_main("Tube Ids sollten unterschiedlich sein.")
            #     return
            #
            # elif self.main_window.plasmidTubesList.check_max_input():
            #     self.main_window.display_qr_from_main("Anzahl von Tubes sollen nicht mehr als 32 sein.")

            else:
                display_msg = "All values look good.\n"
                count_tubes = []
                try:
                    for plasmid, tubes_list in self.experiment_data.plasmid_tubes.items():
                        self.ui_database.adapter.insert_tubes(tubes_list, self.experiment_data.experiment_id, plasmid)
                        print(plasmid + " - " + ', '.join(map(str, tubes_list)))
                        display_msg += f"Created Tubes successfully for {plasmid} : {tubes_list}. \n"
                        count_tubes.append(tubes_list)

                    tube_info_data = self.ui_database.adapter.get_tubes_by_exp_id(self.experiment_data.experiment_id)
                    probe_list = []
                    for tube in tube_info_data:
                        self.tube_information.add_tube(tube['probe_nr'], tube['qr_code'],
                                                       tube['plasmid_nr'])
                        probe_list.append(tube['qr_code'])
                    print(self.tube_information)
                    self.main_window.display_qr_from_main(probe_list)
                    # TODO layout anpassen
                    self.main_window.custom_live_widget.display_tubes_data()
                    # qr_codes_list = self.ui_database.adapter.get_next_qr_codes(len(count_tubes))
                    # for qr_code in qr_codes_list:
                    #     print(qr_code)

                except Exception as ex:
                    display_msg = f"Could not create tubes. \n{ex}"
                    self.show_message_in_dialog(display_msg)
                    return

                # self.nextPage()
                # Load back dashboard
                self.show_message_in_dialog(display_msg)
                exp_sds = ExperimentPreparationWidget(self.ui.vorbereitungStackedTab, self.ui.test_page_home)
                exp_sds.reset_input_of_past_experiments()
                self.main_window.tab_widget_home_dashboard.removeTab(1)
                #load start ent app
                self.main_window.home_dashboard.show_start_button()
                self.main_window.home_dashboard.add_other_page_nav_btns()

                # load live view
                # Add CustomLiveWidget to the layout
                live_widget = CustomLiveWidget(self.ui.test_page_home)
                self.main_window.tab_widget_home_dashboard.addTab(live_widget, "Live")


        elif page_data == 'ShowQrCodeList':
            print()

    def show_message_in_dialog(self, display_msg):
        self.main_window.dialogBoxContents.append(
            self.main_window.dialog.addContent(f"{display_msg}", ContentType.OUTPUT))
        self.main_window.dialog.show()

    def prevPage(self):
        print("prev clicked")
        current_index = self.ui.vorbereitungStackedTab.currentIndex()
        if current_index > 0:
            self.ui.vorbereitungStackedTab.setCurrentIndex(current_index - 1)

    def check_duplicates(self, tubes):
        flat_list = []
        for key, value in tubes.items():
            if isinstance(value, list):
                flat_list.extend(value)
            else:
                flat_list.append(value)
        return len(flat_list) != len(set(flat_list))

    def experiment_creation(self, page_data):
        global exp_data
        # Clear Cache before saving
        self.experiment_data.clear_cache()

        plasmid_list = [str(plasmid) for plasmid in self.ui.plasmidListEV_LE.text().split(',')]
        # If all checks pass, go to the next page
        # Create empty list for each plasmid and saving in dict
        plasmid_dict = {plasmid: None for plasmid in plasmid_list}
        plasmid_dict = {plasmid: i for i, plasmid in enumerate(plasmid_list)}
        # Storing runtime Experiment data

        # Ensure plasmidListEV_LE.text() is not None
        plasmid_text = self.ui.plasmidListEV_LE.text() or ""
        plasmid_list = [str(plasmid) for plasmid in plasmid_text.split(',')]

        data = {
            "exp_id": self.ui.experimentIdLE.text(),
            "firstname": self.ui.nameLE.text(),
            "lastname": self.ui.vornameLE.text(),
            "anz_plasmid": self.ui.anzahlPlasmidLE.text(),
            "anz_tubes": self.ui.anzahlTubesLE.text(),
            "plasmid_list": plasmid_list,
            "date": self.ui.datumLE.date().getDate()
        }

        self.main_window.removeDialogBoxContents()

        # Check for empty fields
        empty_fields = [key for key, value in data.items() if not value and key != 'exp_id']

        if empty_fields:
            self.show_message_in_dialog(f"Eingabe Felder sollen nicht leer sein.")
            return

        # Check if 'anz_plasmid' and 'anz_tubes' are integers
        if not (data['anz_plasmid'].isdigit() and data['anz_tubes'].isdigit()):
            display_msg = "Anzahl Plasmid und Anzahl Tubes sollen Zahlen sein. Bitte Zahlen eingeben.\n"
            self.show_message_in_dialog(display_msg)
            return

        if int(data['anz_tubes']) % 2 != 0:
            display_msg = "Anzahl Tubes soll eine gerade Zahl sein.\n"
            self.show_message_in_dialog(display_msg)
            return

        if int(data['anz_tubes']) > 32 and int(data['anz_tubes']) > 32:
            display_msg = "Anzahl Tubes oder Anzahl Plasmid sollen nicht größer als 32 sein.\n"
            self.show_message_in_dialog(display_msg)
            return

        # Check if the count of plasmids matches 'anz_plasmid'
        if len(plasmid_list) != int(data['anz_plasmid']):
            display_msg = "Anzahl von Plasmid und Plasmid Liste stimmen nicht zu. \n"
            self.show_message_in_dialog(display_msg)
            return

        # Check if 'anz_plasmid' is not greater than 'anz_tubes'
        if int(data['anz_plasmid']) > int(data['anz_tubes']):
            display_msg = "Anzahl von Plasmid soll größer als Anzahl von Tubes sein.\n"
            self.show_message_in_dialog(display_msg)
            return

        try:
            for elem in plasmid_list:
                check_if_plasmid_exists_data = self.ui_database.metadata_adapter.get_plasmid_data_by_nr(elem)
                if check_if_plasmid_exists_data:
                    print("Plasmid data : " + str(check_if_plasmid_exists_data))
                else:
                    raise ValueError(f"Plasmid {elem} existiert nicht. \n")

        except Exception as ex:
            self.show_message_in_dialog(ex)
            return

        try:
            date_str = '-'.join(map(str, data['date']))
            experiment_id = data['exp_id'] or None
            exp_id_data = None

            if experiment_id:
                exp_id_data = self.ui_database.adapter.get_experiment_by_id(experiment_id)

            if exp_id_data is None:
                print(f"{exp_id_data} is None")
                exp_data = self.ui_database.add_experiment(data['firstname'], data['lastname'],
                                                           data['anz_tubes'],
                                                           data['anz_plasmid'], date_str, None)
                self.ui.experimentIdLE.setText(str(exp_data))
                self.experiment_data = ExperimentSingleton(firstname=data['firstname'], lastname=data['lastname'],
                                                           exp_id=exp_data, plasmids=data['plasmid_list'],
                                                           date=data['date'])
                self.current_experiment = CurrentExperimentSingleton(self.experiment_data.experiment_id)
                print(self.main_window.save_cache("exp_id", self.experiment_data.experiment_id))
                self.main_window.cache_data = self.main_window.load_cache()
                print("Exp-data : " + exp_data)
            else:
                print(f"{exp_id_data} is not None")
                print(exp_id_data)
                exp_data = self.ui_database.add_experiment(data['firstname'], data['lastname'],
                                                           data['anz_tubes'],
                                                           data['anz_plasmid'], date_str, experiment_id)
                self.ui.experimentIdLE.setText(str(exp_data))
                self.experiment_data = ExperimentSingleton(firstname=data['firstname'], lastname=data['lastname'],
                                                           exp_id=exp_data, plasmids=data['plasmid_list'],
                                                           date=data['date'])
                print(self.main_window.save_cache("exp_id", self.experiment_data.experiment_id))
                self.current_experiment = CurrentExperimentSingleton(self.experiment_data.experiment_id)
                print("Exp-data : " + exp_data)

                self.main_window.cache_data = self.main_window.load_cache()

            print(self.experiment_data)
            print(self.tube_information)
        except Exception as ex:
            print(f"An error occurred: {ex}")

            # TODO Load all tubes for plasmids and while creating check if the id exists, if exists dont add in db , only add if not
        # plasmid_dict = self.ui_database.get_tubes_data_for_experiment(self.experiment_data.experiment_id)
        # plasmid_probe_dict = {}
        # for item in plasmid_dict:
        #     plasmid_probe_dict[plasmid_dict['probe_nr']] = plasmid_dict['plasmid_nr']
        # print("This is test plasmid_dict : ")
        # print(plasmid_probe_dict)
        # for elem in plasmid_probe_dict:
        #     print(elem)
        self.main_window.plasmidTubesList.displayPlasmidTubes(plasmid_list, None)
        print(data)

        # self.main_window.ui_db.add_experiment()

        self.nextPage()

    def map_prev_next(self, ui):
        ui.vorbereitungPrev.clicked.connect(self.prevPage)
        ui.vorbereitungPrev_2.clicked.connect(self.prevPage)
        ui.vorbereitungPrev_4.clicked.connect(self.prevPage)
        ui.vorbereitungNext.clicked.connect(
            lambda: self.nextPageWithControl("CreateExperiment"))
        ui.probe_to_plasmid_next.clicked.connect(
            lambda: self.nextPageWithControl("AddProbeToPlasmid"))
        ui.vorbereitungWeiter_2.clicked.connect(self.nextPage)
        ui.vorbereitungWeiter_3.clicked.connect(self.nextPage)
