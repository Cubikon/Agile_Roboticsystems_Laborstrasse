from DBService.Control.DatabaseConnection import DatabaseConnection

 # TODO   
    # get tubedate by tubeId
    # zurückgeben=> exp_id plasmidnr,qr_code

class TubeAdapter:
    def __init__(self,db):
        self.db = db

    def insert_tubes(self, probe_nr_list, exp_id, plasmid_nr):
           
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



    # def get_tubes_by_exp_id(self, exp_id):
    #     with self.db as conn:
    #         # SQL-Abfrage, um alle Tubes für die gegebene Experiment-ID zu holen
    #         cursor = conn.execute("SELECT * FROM Tubes WHERE exp_id = ?", (exp_id,))
    #         tubes = cursor.fetchall()

    #         # Konvertieren Sie die Ergebnisse in eine Liste von Dictionaries
    #         tubes_list = []
    #         for tube in tubes:
    #             formatted_qr_code = f"{tube[0]:06d}"  # Fügt führende Nullen hinzu, um eine Länge von 6 zu erreichen

    #             tube_dict = {
    #                 'qr_code': formatted_qr_code,
    #                 'probe_nr': tube[1],
    #                 'exp_id': tube[2],
    #                 'plasmid_nr': tube[3]
    #             }
    #             tubes_list.append(tube_dict)

    #         return tubes_list    
    def get_tubes_by_exp_id(self, exp_id):
        try:
            with self.db as conn:
                print(f"Suche nach Tubes für Experiment-ID: {exp_id}")
                cursor = conn.execute("SELECT * FROM Tubes WHERE exp_id = ?", (exp_id,))
                tubes = cursor.fetchall()

                if not tubes:
                    print(f"Keine Tubes für Experiment-ID {exp_id} gefunden.")
                    return []

                tubes_list = []
                for tube in tubes:
                    formatted_qr_code = f"{tube[0]:06d}"
                    tube_dict = {
                        'qr_code': formatted_qr_code,
                        'probe_nr': tube[1],
                        'exp_id': tube[2],
                        'plasmid_nr': tube[3]
                    }
                    tubes_list.append(tube_dict)
                    print(f"Gefundenes Tube: {tube_dict}")

                return tubes_list
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            return []

  

    def get_tubes(self):
        with self.db as conn:
            # SQL-Abfrage, um alle Tubes für die gegebene Experiment-ID zu holen
            cursor = conn.execute("SELECT * FROM Tubes")
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


    def get_tube_data_by_probe_nr(self, probe_nr):
        with self.db as conn:
            # SQL-Abfrage, um die Daten des Tubes zu holen
            cursor = conn.execute('''
                SELECT 
                    qr_code, 
                    probe_nr, 
                    exp_id, 
                    plasmid_nr
                FROM Tubes 
                WHERE probe_nr = ?
            ''', (probe_nr,))
            tube_data = cursor.fetchone()

            # Überprüfen, ob Daten gefunden wurden
            if tube_data:
                # Formatieren des qr_code
                formatted_qr_code = f"{tube_data[0]:06d}"
                # Erstellen eines Dictionary mit den Tube-Daten
                tube_data_dict = {
                    'qr_code': formatted_qr_code,
                    'probe_nr': tube_data[1],
                    'exp_id': tube_data[2],
                    'plasmid_nr': tube_data[3]
                }
                return tube_data_dict
            else:
                print(f"Kein Tube mit Probe-Nr. {probe_nr} gefunden.")
                return None


    def get_plasmids_for_experiment(self, exp_id):
        with self.db as conn:
            # SQL-Abfrage, um alle Plasmid-Nummern für die gegebene Experiment-ID zu holen
            cursor = conn.execute('''
                     SELECT plasmid_nr
                     FROM Tubes 
                     WHERE exp_id = ?
                 ''', (exp_id,))
            plasmids = cursor.fetchall()

            # Extrahieren Sie die Plasmid-Nummern aus den Ergebnissen
            plasmid_numbers = [plasmid[0] for plasmid in plasmids]

            return plasmid_numbers