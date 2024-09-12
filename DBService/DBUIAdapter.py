from DBService.Control.DatabaseConnection import DatabaseConnection
from DBService.Control.DatabaseAdapter import DatabaseAdapter
from DBService.Control.ExcelImporter import ExcelImporter
from DBService.Control.ExperimentImporter import ExperimentImporter
from DBService.Control.ExperimentAdapter import ExperimentAdapter
from DBService.Control.TubeAdapter import TubeAdapter
from DBService.Control.MetadataAdapter import MetadataAdapter
from DBService.QRGenAdapter import QRGenAdapter
import tkinter as tk
from tkinter import filedialog

class DBUIAdapter:
    def __init__(self):
        self.db = DatabaseConnection("laborstreet_management")
        self.adapter = DatabaseAdapter(self.db)
        self.experiment_adapter=ExperimentAdapter( self.db)
        self.tube_adapter=TubeAdapter( self.db)
        self.metadata_adapter=MetadataAdapter(self.db)
        self.qr_gen = QRGenAdapter(self.adapter)
        # self.importer=ExcelImporter(self.adapter, file_path = 'D:\\Bachelorarbeit\\Plasmid_l.xlsx')
        self.importer = None  # Initialisieren Sie den Importer später

    def add_experiment(self, name, vorname, anz_tubes, anz_plasmid, datum, exp_id):
        return self.experiment_adapter.add_experiment(name, vorname, anz_tubes, anz_plasmid, datum, exp_id)

    def insert_tubes(self, probe_nr_list, exp_id, plasmid_nr):
        self.tube_adapter.insert_tubes(probe_nr_list, exp_id, plasmid_nr)

    def get_tubes_by_exp_id(self,exp_id):
        return(self.tube_adapter.get_tubes_by_exp_id(exp_id))  
    def get_tubes(self):
        return(self.tube_adapter.get_tubes())
    
    def  get_experiment_by_id(self,exp_id):
        return self.experiment_adapter.get_experiment_by_id(exp_id)
    def get_all_experiments(self):
        return(self.experiment_adapter.get_all_experiments())
    def insert_metadaten(self,file_patn):
        self.metadata_adapter.insert_metadaten(file_patn)
    def select_all_from_plasmid(self):
        return self.metadata_adapter.select_all_from_plasmid()

    def get_tubes_data_for_experiment(self,exp_id):
        return self.experiment_adapter.get_tubes_data_for_experiment(exp_id)


    def delete_experiment(self,exp_id):
        self.experiment_adapter.delete_experiment(exp_id)

    def get_tube_data_by_probe_nr(self,probe_nr):
        return self.tube_adapter.get_tube_data_by_probe_nr(probe_nr)
    def get_plasmid_data_by_nr(self,plasmid_nr):
        return self.metadata_adapter.get_plasmid_data_by_nr(plasmid_nr)

    def get_plasmids_for_experiment(self,exp_id):
        return self.tube_adapter.get_plasmids_for_experiment(exp_id)
    def select_file(self):
        root = tk.Tk()
        root.withdraw()  # Verstecken Sie das Hauptfenster
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        return file_path
        
    def create_qr_code(self, total: int):
        self.db.create_table()
        return [self.qr_gen.create_tube_qrcode() for _ in range(total)]

    # def insert_metadaten(self):
    #     file_path=self.select_file()
    #     if file_path:
    #         self.importer=ExcelImporter(self.adapter,file_path)
    #         self.importer.import_data()
    #     else:
    #         print("Keine Datei ausgewählt.")

    def insert_experiment_data(self):
        self.experiment_adapter.insert_experiment_data()



    def delete_all_experiment(self):
        self.adapter.delete_all_experiments()


