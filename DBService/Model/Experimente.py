class Experimente:
    """ 
    Diese Klasse repräsentiert ein Experiment im Kontext eines Labormanagementsystems.
    
    Jedes Experiment-Objekt speichert  Informationen wie die eindeutige ID des Experiments,
    den Namen und Vornamen des durchführenden Laboranten, die Anzahl der verwendeten Tubes und Plasmide,
    sowie das Datum, an dem das Experiment durchgeführt wurde.

    Die Klasse bietet auch Methoden zur String-Repräsentation (`__str__`) für eine benutzerfreundliche Ausgabe
    und zur offiziellen Darstellung (`__repr__`) für Debugging-Zwecke.
    """
    def __init__(self, exp_id, name, vorname, anz_tubes, anz_plasmid,datum):
        self.exp_id = exp_id
        self.name = name
        self.vorname = vorname
        self.anz_tubes = anz_tubes
        self.anz_plasmid = anz_plasmid
        self.datum = datum
        
    def __str__(self):
        return f"Experiment ID: {self.exp_id}, Name: {self.name}, Vorname: {self.vorname}, Anzahl Tubes: {self.anz_tubes}, Anzahl Plasmid: {self.anz_plasmid}, Datum: {self.datum}"

    # Optional: Für eine detailliertere Darstellung in Debugging-Situationen
    def __repr__(self):
        return f"Experimente(exp_id={self.exp_id}, name={self.name}, vorname={self.vorname}, anz_tubes={self.anz_tubes}, anz_plasmid={self.anz_plasmid}, datum={self.datum})"   