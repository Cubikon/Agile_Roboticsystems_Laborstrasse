class Experiment:
    def __init__(self, exp_id, name, vorname, anz_tubes, anz_plasmid, video_id, datum, anz_fehler, bemerkung):
        self.exp_id = exp_id
        self.name = name
        self.vorname = vorname
        self.anz_tubes = anz_tubes
        self.anz_plasmid = anz_plasmid
        self.video_id = video_id
        self.datum = datum
        self.anz_fehler = anz_fehler
        self.bemerkung = bemerkung

    def __str__(self):
        return (f"Experiment ID: {self.exp_id}, Name: {self.name}, Vorname: {self.vorname}, "
                f"Anzahl Tubes: {self.anz_tubes}, Anzahl Plasmid: {self.anz_plasmid}, "
                f"Datum: {self.datum}, Video ID: {self.video_id}, Anzahl Fehler: {self.anz_fehler}, "
                f"Bemerkung: {self.bemerkung}")
