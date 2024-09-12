import pandas as pd

class TubeMetaDatenImporter:
    """
    Diese Klasse dient zum Importieren von Metadaten zu Plasmiden aus einer Excel-Datei.

    Der Importer liest die Daten aus der angegebenen Excel-Datei und speichert die Informationen
    zu verschiedenen Attributen von Plasmiden wie Plasmidnummer, Vektor, Insert, Sequenznummer,
    Name, Datum der Maxi-Präparation, Quelle und Konstruktionsdatum.

    Die Klasse erwartet, dass die Excel-Datei spezifische Spaltennamen enthält, die den Attributen
    eines Plasmids entsprechen.

    Methoden:
    - __init__: Initialisiert den Importer mit dem Pfad zur Excel-Datei.
    - import_data: Liest die Daten aus der Excel-Datei und speichert sie in entsprechenden Listen.
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.plasmid_nr = []
        self.vektor = []
        self.insert = []
        self.sequenz_nr = []
        self.name = []
        self.datum_maxi = []
        self.quelle = []
        self.konstruktion_datum = []

    def import_data(self):
        # Excel-Datei importieren
        df = pd.read_excel(self.file_path)

        # Überprüfe, ob die benötigten Spalten vorhanden sind
        required_columns = ['Plasmid_nr', 'Vektor', 'Insert', 'Sequnez_nr', 'Name', 'Datum_maxi', 'Quelle', 'Konstruktion_datum']
        for column in required_columns:
            if column not in df.columns:
                print(f"Die erforderliche Spalte '{column}' ist nicht in der Excel-Datei vorhanden.")
                return

        # Daten aus der Excel-Datei in Variablen zuweisen
        self.plasmid_nr = df['Plasmid_nr'].tolist()
        self.vektor = df['Vektor'].tolist()
        self.insert = df['Insert'].tolist()
        self.sequenz_nr = df['Sequnez_nr'].tolist()
        self.name = df['Name'].tolist()
        self.datum_maxi = df['Datum_maxi'].tolist()
        self.quelle = df['Quelle'].tolist()
        self.konstruktion_datum = df['Konstruktion_datum'].tolist()

        # Ausgabe der Daten
        for i in range(len(self.plasmid_nr)):
            print(f"Plasmid Nr: {self.plasmid_nr[i]}, Vektor: {self.vektor[i]}, Insert: {self.insert[i]}, Sequenz Nr: {self.sequenz_nr[i]}, Name: {self.name[i]}, Datum Maxi: {self.datum_maxi[i]}, Quelle: {self.quelle[i]}, Konstruktion Datum: {self.konstruktion_datum[i]}")

