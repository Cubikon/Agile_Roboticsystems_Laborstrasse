import pandas as pd
from DBService.Control.DatabaseAdapter import DatabaseAdapter
from DBService.Control.DatabaseConnection import DatabaseConnection

from DBService.Model.Experiment import Experiment


class ExperimentImporter:
    """
    Diese Klasse dient zum Importieren von Experimentdaten aus einer Excel-Datei in das Labormanagementsystem.

    Der Importer liest die Daten aus der angegebenen Excel-Datei, erstellt für jede Zeile ein Experiment-Objekt
    und speichert diese in einer Liste. Anschließend werden die Experimente in die Datenbank eingefügt.

    Die Klasse erwartet, dass die Excel-Datei spezifische Spaltennamen enthält, die den Attributen eines Experiments
    entsprechen, wie exp_id, name, vorname, anz_tubes, video_id, datum, anz_fehler und bemerkung.

    Methoden:
    - __init__: Initialisiert den Importer mit einem Datenbankadapter und dem Pfad zur Excel-Datei.
    - import_data: Liest die Daten aus der Excel-Datei, erstellt Experiment-Objekte und fügt sie in die Datenbank ein.
    """
    def __init__(self, file_path):
        self.db = DatabaseConnection("laborstreet_management")
        self.adapter = DatabaseAdapter(self.db)
        self.file_path = file_path
        self.experiments = []

    # def import_data(self):
    #     df = pd.read_excel(self.file_path)
    #     required_columns = ['exp_id', 'name', 'vorname', 'anz_tubes', 'video_id', 'datum', 'anz_fehler', 'bemerkung']
    #
    #     ausgabe_data = []
    #
    #     for column in required_columns:
    #         if column not in df.columns:
    #             ausgabe_data.append(f"Die erforderliche Spalte '{column}' ist nicht in der Excel-Datei vorhanden.")
    #             return ausgabe_data
    #
    #     for index, row in df.iterrows():
    #         experiment = Experiment(row['exp_id'], row['name'], row['vorname'], row['anz_tubes'], row['video_id'], row['datum'], row['anz_fehler'], row['bemerkung'])
    #         print(experiment)
    #         self.experiments.append(experiment)
    #
    #     # Ausgabe der Daten
    #     for experiment in self.experiments:
    #         print("_______________________________Imported_________________________________________________")
    #         ausgabe_data.append(f"Experiment ID: {experiment.exp_id}, Name: {experiment.name}, Vorname: {experiment.vorname}, Anzahl Tubes: {experiment.anz_tubes}, Video ID: {experiment.video_id}, Datum: {experiment.datum}, Anzahl Fehler: {experiment.anz_fehler}, Bemerkung: {experiment.bemerkung}")
    #         self.adapter.insert_experiment(experiment)
    #     return ausgabe_data



    def import_data(self):
            df = pd.read_excel(self.file_path)
            required_columns = ['exp_id', 'name', 'vorname', 'anz_tubes', 'anz_plasmid', 'datum', 'video_id',
                                'anz_fehler', 'bemerkung']

            ausgabe_data = []

            for column in required_columns:
                if column not in df.columns:
                    ausgabe_data.append(f"Die erforderliche Spalte '{column}' ist nicht in der Excel-Datei vorhanden.")
                    return ausgabe_data

            for index, row in df.iterrows():
                experiment = Experiment(row['exp_id'], row['name'], row['vorname'], row['anz_tubes'],
                                        row['anz_plasmid'], row['video_id'], row['datum'], row['anz_fehler'], row['bemerkung'])

                self.experiments.append(experiment)

            # Ausgabe der Daten
            for experiment in self.experiments:
                ausgabe_data.append(
                    f"Experiment ID: {experiment.exp_id}, Name: {experiment.name}, Vorname: {experiment.vorname}, Anzahl Tubes: {experiment.anz_tubes}, Anzahl Plasmid: {experiment.anz_plasmid}, Datum: {experiment.datum},Video ID: {experiment.video_id},  Anzahl Fehler: {experiment.anz_fehler}, Bemerkung: {experiment.bemerkung}")
                self.adapter.insert_experiment(experiment)

            return ausgabe_data