from DBService.Model.Experiment import Experiment
from DBService.Model.Experimente import Experimente
import pandas as pd

class DatabaseAdapter:
    def __init__(self, db):
        self.db = db
        self.last_qr_code_index = 0  # Initialisieren den Zähler

    def insert_tubes(self, probe_nr_list, exp_id, plasmid_nr):
        # Überprüfen, ob die Tabelle existiert
        if not self.does_table_exist("Tubes"):
            print("Tabelle 'Tubes' existiert nicht. Sie wird erstellt.")
            self.db.create_tubes_table()
        else:
            print("Tabelle 'Tubes' existiert bereits.")

        with self.db as conn:
            for probe_nr in probe_nr_list:
                # Generiere qr_code basierend auf probe_nr
                qr_code = f"{probe_nr:06d}"  # Füllt die Zahl mit führenden Nullen auf 6 Stellen auf
                # Fügen Sie das Tube in die Datenbank ein
                conn.execute('''
                    INSERT INTO Tubes (qr_code, probe_nr, exp_id, plasmid_nr)
                    VALUES (?, ?, ?, ?)
                ''', (qr_code, probe_nr, exp_id, plasmid_nr))
                print(f"Tube mit QR-Code {qr_code} hinzugefügt.")

    def get_all_tubes(self):
        with self.db as conn:
            # SQL-Abfrage, um alle Einträge aus der Tubes Tabelle zu holen
            cursor = conn.execute("SELECT * FROM Tubes")
            tubes = cursor.fetchall()

            # Optional: Konvertieren Sie die Ergebnisse in eine Liste von Objekten oder Dictionaries
            tubes_list = []
            for tube in tubes:
                formatted_qr_code = f"{tube[0]:06d}"  # Fügt führende Nullen hinzu, um eine Länge von 6 zu erreichen

                tube_dict = {
                    'qr_code': formatted_qr_code,
                    'probe_nr': tube[1],
                    'exp_id': tube[2],
                    'plasmid_nr': tube[3]
                }
                tubes_list.append(tube_dict)

            return tubes_list
        
    def get_tubes_by_exp_id(self, exp_id):
        with self.db as conn:
            # SQL-Abfrage, um alle Tubes für die gegebene Experiment-ID zu holen
            cursor = conn.execute("SELECT * FROM Tubes WHERE exp_id = ?", (exp_id,))
            tubes = cursor.fetchall()

            # Konvertieren Sie die Ergebnisse in eine Liste von Dictionaries
            tubes_list = []
            for tube in tubes:
                formatted_qr_code = f"{tube[0]:06d}"  # Fügt führende Nullen hinzu, um eine Länge von 6 zu erreichen

                tube_dict = {
                    'qr_code': formatted_qr_code,
                    'probe_nr': tube[1],
                    'exp_id': tube[2],
                    'plasmid_nr': tube[3]
                }
                tubes_list.append(tube_dict)

            return tubes_list
        

    def drop_table_tube_qrcode(self):
        with self.db as conn:
            # Löschen der Tabelle TubeQrcode
            conn.execute("DROP TABLE IF EXISTS TubeQrcode")

    def insert_data(self, tubeQrcode):  
        with self.db as conn:
            conn.execute("INSERT INTO TubeQrcode (qr_code, datum) VALUES (?, ?)",
                         (tubeQrcode.qr_code, tubeQrcode.datum))

    def get_last_qr_code(self):
        if not self.does_table_exist("TubeQrcode"):
            print("Tabelle 'TubeQrcode' existiert nicht. Sie wird erstellt.")
            self.db.create_table()
        else:
            print("Tabelle 'TubeQrcode' existiert bereits.")
        with self.db as conn:
            row = conn.execute("SELECT MAX(qr_code) FROM TubeQrcode").fetchone()
            return int(row[0]) if row[0] else 0

    def get_last_qr_code(self):
        if not self.does_table_exist("TubeQrcode"):
            print("Tabelle 'TubeQrcode' existiert nicht. Sie wird erstellt.")
            self.db.create_table()
        else:
            print("Tabelle 'TubeQrcode' existiert bereits.")
        with self.db as conn:
            row = conn.execute("SELECT MAX(qr_code) FROM TubeQrcode").fetchone()
            return int(row[0]) if row[0] else 0

    def select_all_from_tubeqrcode(self):
        # Überprüfen, ob die Tabelle existiert
        if not self.does_table_exist("Tubes"):
            print("Tabelle 'Tubes' existiert nicht. Sie wird erstellt.")
            self.db.create_tubes_table()
            with self.db as conn:
                rows = conn.execute("SELECT * FROM TubeQrcode").fetchall()
                for row in rows:
                    formatted_qr_code = str(row[0]).zfill(6)
                    print((formatted_qr_code, row[1]))
        else:
            print("Tabelle 'Tubes' existiert bereits.")

    def get_next_qr_codes(self, count):
        with self.db as conn:
            # Abrufen der QR-Codes ab der letzten Position
            cursor = conn.execute("SELECT * FROM TubeQrcode ORDER BY qr_code LIMIT ? OFFSET ?",
                                  (count, self.last_qr_code_index))
            qr_codes = cursor.fetchall()

            # Aktualisieren Sie den Zähler
            self.last_qr_code_index += len(qr_codes)

            # Formatieren und zurückgeben der QR-Codes
            formatted_qr_codes = [(str(row[0]).zfill(6), row[1]) for row in qr_codes]
            return formatted_qr_codes

    def insert_plasmid(self, plasmid):
        # Überprüfen, ob die Tabelle existiert
        if not self.does_table_exist("Plasmid"):
            print("Tabelle 'Plasmid' existiert nicht. Sie wird erstellt.")
            self.db.create_plasmid_table()
        else:
            print("Tabelle 'Plasmid' existiert bereits.")

        with self.db as conn:
            # Überprüfen und konvertieren Sie den Datentyp von plasmid.name
            name = str(plasmid.name) if plasmid.name is not None else None

            # Konvertiert Datumswerte in Strings
            datum_maxi = plasmid.datum_maxi.strftime('%Y-%m-%d') if plasmid.datum_maxi is not None else None
            konstruktion_datum = plasmid.konstruktion_datum.strftime(
                '%Y-%m-%d') if plasmid.konstruktion_datum is not None else None

            # Füge das Plasmid in die Datenbank ein
            conn.execute('''
            INSERT INTO Plasmid (plasmid_nr, vektor, "insert", sequenz_nr, name, datum_maxi, quelle, konstruktion_datum)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
            plasmid.plasmid_nr, plasmid.vektor, plasmid.insert, plasmid.sequenz_nr, name, datum_maxi, plasmid.quelle,
            konstruktion_datum))

    def add_experiment(self, name, vorname, anz_tubes, anz_plasmid, datum, exp_id_param):
        self.add_laborant(name,vorname)
        exp_anzahl = self.get_experiment_count_for_laborant(name)
        if exp_anzahl is not None:
            print("Experiments_anzahl: " + str(exp_anzahl))
        else:
            print("Kein Laborant mit dem Namen " + name + " gefunden.")

        if not exp_id_param:
            exp_id = f"{name}{exp_anzahl + 1}"
        else:
            exp_id = exp_id_param

        if not self.does_table_exist("Experiment"):
            print("Tabelle 'Experiment' existiert nicht. Sie wird erstellt.")
            # self.db.crt_experiment()
            self.db.create_experiment_table()

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

    def get_experiment_count_for_laborant(self, name):
        with self.db as conn:
            print(f"Suche nach Experimenten für Laborant: {name}")
            cursor = conn.execute('''
                    SELECT anz_exp FROM Laborant WHERE name = ?
                ''', (name,))
            result = cursor.fetchone()
            if result:
                print(f"Anzahl der Experimente gefunden: {result[0]}")
                return result[0]
            else:
                print("Kein Laborant mit diesem Namen gefunden.")
                return None

    def increment_experiment_count_for_laborant(self, name):

        with self.db as conn:
            # Erhöhe anz_exp um 1 für den spezifischen Laboranten
            conn.execute('''
                UPDATE Laborant
                SET anz_exp = anz_exp + 1
                WHERE name = ?
            ''', (name,))
            print(f"Experimentanzahl für Laborant {name} wurde um 1 erhöht.")

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

    def add_laborant(self, name, vorname):
        experimentsanzahl = 0
        # Überprüfen, ob die Tabelle existiert
        if not self.does_table_exist("Laborant"):
            print("Tabelle 'Laborant' existiert nicht. Sie wird erstellt.")
            self.db.create_laborant_table()
        else:
            print("Tabelle 'Laborant' existiert bereits.")

        with self.db as conn:
            # Füge den neuen Laboranten in die Tabelle ein
            conn.execute('''
                        INSERT INTO Laborant (name, vorname, anz_exp)
                        VALUES (?, ?, ?)
                    ''', (name, vorname, experimentsanzahl))
            print(f"Laborant {name} {vorname} mit {experimentsanzahl} Experimenten wurde hinzugefügt.")

    def get_laborant_count(self):
        with self.db as conn:
            cursor = conn.execute('SELECT COUNT(*) FROM Laborant')
            result = cursor.fetchone()
            if result:
                return result[0]  # Gibt die Anzahl der Laboranten zurück
            else:
                return 0  # Keine Laboranten gefunden

    def insert_experiment(self, experiment):
        if not self.does_table_exist("Experiment"):
            print("Tabelle 'Experiment' existiert nicht. Sie wird erstellt.")
            self.db.create_experiment_table()
        with self.db as conn:
            # video_id in einen String
            video_id_str = str(experiment.video_id)

            # konvert das Datum in einen String im Format YYYY-MM-DD
            datum_str = experiment.datum.strftime('%Y-%m-%d') if experiment.datum is not None else None

            # Überprüfen, ob das Experiment bereits existiert
            cursor = conn.execute('SELECT COUNT(*) FROM Experiment WHERE exp_id = ?', (experiment.exp_id,))
            exists = cursor.fetchone()[0] > 0

            if exists:
                # Aktualisiere das vorhandene Experiment
                conn.execute('''
                        UPDATE Experiment
                        SET name = ?, vorname = ?, anz_tubes = ?,anz_plasmid=?, datum = ?, video_id = ?,  anz_fehler = ?, bemerkung = ?
                        WHERE exp_id = ?
                    ''', (experiment.name, experiment.vorname, experiment.anz_tubes, video_id_str, datum_str,
                          experiment.anz_fehler, experiment.bemerkung, experiment.exp_id))
            else:
                # ein neues Experiment einfügen
                conn.execute('''
                        INSERT INTO Experiment (exp_id, name, vorname, anz_tubes,anz_plasmid, datum, video_id, anz_fehler, bemerkung)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)
                    ''', (
                experiment.exp_id, experiment.name, experiment.vorname, experiment.anz_tubes,experiment.anz_plasmid, datum_str,video_id_str,
                experiment.anz_fehler, experiment.bemerkung))

    def get_experiments(self):
        with self.db as conn:
            cursor = conn.execute('SELECT * FROM Experiment')
            experiments = cursor.fetchall()

            # Optional: Konvertiert die Ergebnisse in eine Liste von Experiment-Objekten
            experiment_list = []
            for exp in experiments:
                experiment_obj = Experimente(exp_id=exp[0], name=exp[1], vorname=exp[2], anz_tubes=exp[3],
                                             anz_plasmid=exp[4], datum=exp[5])
                experiment_list.append(experiment_obj)
            return experiment_list

    # def insert_experiment(self, experiment):
    #     if not self.does_table_exist("Experiment"):
    #         print("Tabelle 'Experiment' existiert nicht. Sie wird erstellt.")
    #         self.db.create_experiment_table()
    #     else:
    #         print("Tabelle 'Experiment' existiert bereits.")
    #     with self.db as conn:
    #
    #         # video_id in einen String
    #         video_id_str = str(experiment.video_id)
    #
    #         # konvert das Datum in einen String im Format YYYY-MM-DD
    #         datum_str = experiment.datum.strftime('%Y-%m-%d') if experiment.datum is not None else None
    #
    #         # Überprüfen, ob das Experiment bereits existiert
    #         cursor = conn.execute('SELECT COUNT(*) FROM Experiment WHERE exp_id = ?', (experiment.exp_id,))
    #         exists = cursor.fetchone()[0] > 0
    #
    #         if exists:
    #             # Aktualisiere das vorhandene Experiment
    #             conn.execute('''
    #                 UPDATE Experiment
    #                 SET name = ?, vorname = ?, anz_tubes = ?, video_id = ?, datum = ?, anz_fehler = ?, bemerkung = ?
    #                 WHERE exp_id = ?
    #             ''', (experiment.name, experiment.vorname, experiment.anz_tubes, video_id_str, datum_str, experiment.anz_fehler, experiment.bemerkung, experiment.exp_id))
    #         else:
    #             # ein neues Experiment einfügen
    #             conn.execute('''
    #                 INSERT INTO Experiment (exp_id, name, vorname, anz_tubes, video_id, datum, anz_fehler, bemerkung)
    #                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    #             ''', (experiment.exp_id, experiment.name, experiment.vorname, experiment.anz_tubes, video_id_str, datum_str, experiment.anz_fehler, experiment.bemerkung))
    #
    def delete_all_experiments(self):
        with self.db as conn:
            # alle Einträge in der Tabelle Experiment löschen
            conn.execute('DELETE FROM Experiment')
            print("Alle Experimente wurden gelöscht.")

    def select_all_from_plasmid(self):
        print("_______________Plasmid__________")
        with self.db as conn:
            rows = conn.execute("SELECT * FROM Plasmid").fetchall()
            for row in rows:
                print(row)

    def get_all_experiments(self):
        with self.db as conn:
            cursor = conn.execute('SELECT * FROM Experiment')
            experiments = cursor.fetchall()

            # Optional: Konvertiere die Ergebnisse in eine Liste von Experiment-Objekten
            experiment_list = []
            for exp in experiments:
                experiment_obj = Experiment(exp_id=exp[0], name=exp[1], vorname=exp[2], anz_tubes=exp[3],anz_plasmid=exp[4],
                                             datum=exp[5],video_id=exp[6], anz_fehler=exp[7], bemerkung=exp[8])
                experiment_list.append(experiment_obj)

            return experiment_list

    def does_table_exist(self, table_name):
        with self.db as conn:
            result = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                                  (table_name,)).fetchone()
            return result is not None
