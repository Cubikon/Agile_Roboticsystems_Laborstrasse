import random
from faker import Faker
import pandas as pd

__author__ = 'Ujwal Subedi'
__date__ = '01/12/2023'
__version__ = '1.0'
__last_changed__ = '01/12/2023'


class DummyDataGenerator:
    """
    Generate Dummy Data for Experiment Table as well as Plasmid Metadata Table.
    """

    def __init__(self):
        self.fake = Faker()
        self.exp_data = []
        self.plasmid_data = []

    def add_entry_experiment(self, exp_id, name, vorname, anz_tubes, video_id, datum, anz_fehler, bemerkung):
        self.exp_data.append([exp_id, name, vorname, anz_tubes, video_id, datum, anz_fehler, bemerkung])

    def generate_random_entries_experiment(self, num_entries):
        for _ in range(num_entries):
            exp_id = self.fake.user_name() + str(random.randint(1, 100))
            name = self.fake.last_name()
            vorname = self.fake.first_name()
            anz_tubes = random.randint(10, 32)
            video_id = random.randint(100, 500)
            datum = self.fake.date(pattern="%d/%m/%Y")
            anz_fehler = random.randint(0, 5)
            bemerkung = random.choice(['G', 'B', 'A'])

            self.add_entry_experiment(exp_id, name, vorname, anz_tubes, video_id, datum, anz_fehler, bemerkung)

    def to_dataframe_experiment(self):
        return pd.DataFrame(self.exp_data,
                            columns=['exp_id', 'name', 'vorname', 'anz_tubes', 'video_id', 'datum', 'anz_fehler',
                                     'bemerkung'])

    def add_entry_plasmid(self, plasmid_nr, vektor, insert, sequnez_nr, name, datum_maxi, quelle, konstruktion_datum):
        self.plasmid_data.append([plasmid_nr, vektor, insert, sequnez_nr, name, datum_maxi, quelle, konstruktion_datum])

    def generate_random_entries_plasmid(self, num_entries):
        for _ in range(num_entries):
            plasmid_nr = 'PHB' + str(random.randint(100, 999))
            vektor = 'pCDNA' + str(random.randint(1, 5)) + ' FRT TO mit Rho-Tag'
            insert = self.fake.word()
            sequnez_nr = self.fake.word()
            name = 'SB' + str(random.randint(100, 999))
            datum_maxi = self.fake.date(pattern="%d/%m/%Y")
            quelle = self.fake.name()
            konstruktion_datum = self.fake.date(pattern="%d/%m/%Y")

            self.add_entry_plasmid(plasmid_nr, vektor, insert, sequnez_nr, name, datum_maxi, quelle, konstruktion_datum)

    def to_dataframe_plasmid(self):
        return pd.DataFrame(self.plasmid_data,
                            columns=['Plasmid_nr', 'Vektor', 'Insert', 'Sequnez_nr', 'Name', 'Datum_maxi', 'Quelle',
                                     'Konstruktion_datum'])


# Usage:
generator = DummyDataGenerator()
generator.generate_random_entries_experiment(15)
df = generator.to_dataframe_experiment()
