
       

from DBService.Control.DatabaseAdapter import DatabaseAdapter


class LaborantAdapter:
        
    def __init__(self,db):
           self.db=db
           self.database_adapter = DatabaseAdapter(self.db)

           print()
        

    def add_laborant(self, name, vorname):
                experimentsanzahl=0
                
                # Überprüfen, ob die Tabelle existiert
                if not self.database_adapter.does_table_exist("Laborant"):
                    print("Tabelle 'Laborant' existiert nicht. Sie wird erstellt.")
                    
                else:
                    print("Tabelle 'Laborant' existiert bereits.")

                with self.db as conn:
                    # Füge den neuen Laboranten in die Tabelle ein
                    conn.execute('''
                        INSERT INTO Laborant (name, vorname, anz_exp)
                        VALUES (?, ?, ?)
                    ''', (name, vorname, experimentsanzahl))
                    print(f"Laborant {name} {vorname} mit {experimentsanzahl} Experimenten wurde hinzugefügt.") 


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


    def get_laborant_count(self):
        with self.db as conn:
            cursor = conn.execute('SELECT COUNT(*) FROM Laborant')
            result = cursor.fetchone()
            if result:
                return result[0]  # Gibt die Anzahl der Laboranten zurück
            else:
                print("Kein Laborant")
                return 0  # Keine Laboranten gefunden           
    


    def does_laborant_exist(self, name):
        with self.db as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM Laborant WHERE name = ?", (name,))
            count = cursor.fetchone()[0]
            return count > 0
