import tkinter
from tkinter import filedialog
from DBService.Control.DatabaseConnection import DatabaseConnection
from DBService.Control.DatabaseAdapter import DatabaseAdapter
from DBService.Control.ExperimentImporter import ExperimentImporter
from DBService.Control.LaborantAdapter import LaborantAdapter
from DBService.Model.Experiment import Experiment
from DBService.Model.Experimente import Experimente


class ExperimentAdapter:
    def __init__(self, db):
        self.experiment_importer = None
        self.db = db
        # self.db = DatabaseConnection("laborstreet_management")
        self.database_adapter = DatabaseAdapter(self.db)
        self.ensure_tables_exist()
        self.laborant_adapter = LaborantAdapter(self.db)

    def ensure_tables_exist(self):
        if not self.database_adapter.does_table_exist("Laborant"):
            self.db.create_laborant_table()
            print("Tabelle 'Laborant' wurde erstellt.")

        if not self.database_adapter.does_table_exist("Tubes"):
            self.db.create_tubes_table()
            print("Tabelle 'Tubes' wurde erstellt.")

        if not self.database_adapter.does_table_exist("Experiment"):
            self.db.create_experiment_table()
            print("Tabelle 'Experiment' wurde erstellt.")

    def add_experiment(self, name, vorname, anz_tubes, anz_plasmid, datum, exp_id_param):
        if self.laborant_adapter.does_laborant_exist(name):
            print(f"Ein Laborant mit dem Namen {name} existiert.")
        else:
            self.laborant_adapter.add_laborant(name, vorname)

            print(f"Kein Laborant mit dem Namen {name} gefunden.")
        exp_anzahl = self.laborant_adapter.get_experiment_count_for_laborant(name)
        if exp_anzahl is not None:
            print("Experiments_anzahl: " + str(exp_anzahl))
        else:
            print("Kein Laborant mit dem Namen " + name + " gefunden.")

        if not exp_id_param:
            exp_id = f"{name}{exp_anzahl + 1}"
        else:
            exp_id = exp_id_param

        # if not self.database_adapter("Experiment"):
        #     print("Tabelle 'Experiment' existiert nicht. Sie wird erstellt.")
        #     # self.db.crt_experiment()
        #     self.db.create_experiment_table()

        with self.db as conn:
            cursor = conn.execute('SELECT COUNT(*) FROM Experiment WHERE exp_id = ?', (exp_id,))
            exists = cursor.fetchone()[0] > 0

            if exists:
                conn.execute('''
                        UPDATE Experiment
                        SET name = ?, vorname = ?, anz_tubes = ?, anz_plasmid = ?, datum = ?
                        WHERE exp_id = ?
                    ''', (name, vorname, anz_tubes, anz_plasmid, datum, exp_id))
                print(f"Experiment mit ID {exp_id} wurde aktualisiert.")
            else:
                conn.execute('''
                        INSERT INTO Experiment (exp_id, name, vorname, anz_tubes, anz_plasmid, datum)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (exp_id, name, vorname, anz_tubes, anz_plasmid, datum))
                print(f"Experiment mit ID {exp_id} wurde hinzugefügt.")

                # Erhöhe anz_exp um 1 für den spezifischen Laboranten
                conn.execute('''
                        UPDATE Laborant
                        SET anz_exp = anz_exp + 1
                        WHERE name = ?
                    ''', (name,))
                print(f"Experimentanzahl für Laborant {name} wurde um 1 erhöht.")

        return exp_id

    def get_experiment_by_id(self, exp_id):
        with self.db as conn:
            cursor = conn.execute('SELECT * FROM Experiment WHERE exp_id = ?', (exp_id,))
            result = cursor.fetchone()

            if result:
                # Optional: Konvertieren Sie das Ergebnis in ein Experiment-Objekt
                experiment = Experimente(exp_id=result[0], name=result[1], vorname=result[2], anz_tubes=result[3],
                                         anz_plasmid=result[4], datum=result[5])
                return experiment
            else:
                print(f"Kein Experiment mit der ID {exp_id} gefunden.")
                return None
                # Weitere Methoden für CRUD-Operationen

    def get_all_experiments(self):

        with self.db as conn:
            cursor = conn.execute('SELECT * FROM Experiment')
            experiments = cursor.fetchall()

            # Optional: Konvertiere die Ergebnisse in eine Liste von Experiment-Objekten
            experiment_list = []
            for exp in experiments:
                experiment_obj = Experiment(exp_id=exp[0], name=exp[1], vorname=exp[2], anz_tubes=exp[3],
                                            video_id=exp[4], datum=exp[5], anz_fehler=exp[6], bemerkung=exp[7])
                experiment_list.append(experiment_obj)

            return experiment_list

    def delete_all_experiment(self):
        with self.db as conn:
            # alle Einträge in der Tabelle Experiment löschen
            conn.execute('DELETE FROM Experiment')
            print("Alle Experimente wurden gelöscht.")

    def get_tubes_data_for_experiment(self, exp_id):
        try:
            with self.db as conn:
                cursor = conn.execute('''
                    SELECT 
                        t.probe_nr, 
                        t.qr_code, 
                        t.plasmid_nr, 
                        p.vektor, 
                        p."insert", 
                        p.name, 
                        e.vorname, 
                        e.exp_id, 
                        e.datum, 
                        e.anz_fehler
                    FROM Tubes t
                    INNER JOIN Plasmid p ON t.plasmid_nr = p.plasmid_nr
                    INNER JOIN Experiment e ON t.exp_id = e.exp_id
                    WHERE t.exp_id = ?
                ''', (exp_id,))
                tubes_data = cursor.fetchall()
                print(tubes_data)
                tubes_data_list = []
                for data in tubes_data:
                    tube_data_dict = {
                        'probe_nr': data[0],
                        'qr_code': f"{data[1]:06d}",
                        'plasmid_nr': data[2],
                        'vektor': data[3],
                        'insert': data[4],
                        'name': data[5],
                        'vorname': data[6],
                        'exp_id': data[7],
                        'datum': data[8],
                        'anz_fehler': data[9]
                    }
                    tubes_data_list.append(tube_data_dict)
                print(tubes_data_list)
                return tubes_data_list
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            return []

    def delete_experiment(self, exp_id):
        try:
            with self.db as conn:
                # Überprüfe, ob das Experiment existiert
                cursor = conn.execute("SELECT COUNT(*) FROM Experiment WHERE exp_id = ?", (exp_id,))
                experiment_exists = cursor.fetchone()[0] > 0

                if not experiment_exists:
                    print(f"Kein Experiment mit ID {exp_id} gefunden.")
                    return

                # Überprüfe, ob das Experiment Tubes hat
                cursor = conn.execute("SELECT COUNT(*) FROM Tubes WHERE exp_id = ?", (exp_id,))
                tube_count = cursor.fetchone()[0]

                if tube_count > 0:
                    # Löschen aller Tubes, die mit dem Experiment verknüpft sind
                    conn.execute("DELETE FROM Tubes WHERE exp_id = ?", (exp_id,))
                    print(f"Alle Tubes für Experiment-ID {exp_id} wurden gelöscht.")
                else:
                    print(f"Keine Tubes für Experiment-ID {exp_id} gefunden.")

                # Löschen des Experiments
                conn.execute("DELETE FROM Experiment WHERE exp_id = ?", (exp_id,))
                print(f"Experiment mit ID {exp_id} wurde gelöscht.")

        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            
    def insert_experiment_data(self,file_path):
        # file_path = self.select_file()

        if file_path:
            # eine Instanz des ExperimentImporters mit dem ausgewählten Dateipfad
            self.experiment_importer = ExperimentImporter(file_path,)
            #die Methode import_data auf, um die Daten zu importieren
            return self.experiment_importer.import_data()
        else:
            return "Keine Datei ausgewählt."
        
    def select_file(self):
        root = tkinter.Tk()
        root.withdraw()  # Verstecken Sie das Hauptfenster
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        return file_path