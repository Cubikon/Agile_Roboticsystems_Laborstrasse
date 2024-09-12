class Plasmid:
    """
    Diese Klasse repräsentiert ein Plasmid und seine zugehörigen Daten.

    Diese Klasse speichert verschiedene Attribute eines Plasmids, wie die Plasmidnummer, den Vektor,
    das Insert, die Sequenznummer, den Namen des Plasmids, das Datum der Maxi-Präparation, die Quelle
    des Plasmids und das Datum der Konstruktion.
    """
    def __init__(self, plasmid_nr=None, vektor=None, insert=None, sequenz_nr=None, name=None, datum_maxi=None, quelle=None, konstruktion_datum=None):
        self.plasmid_nr = plasmid_nr
        self.vektor = vektor
        self.insert = insert
        self.sequenz_nr = sequenz_nr
        self.name = name
        self.datum_maxi = datum_maxi
        self.quelle = quelle
        self.konstruktion_datum = konstruktion_datum
