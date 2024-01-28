import sqlite3
__author__ = 'Wissam Alamareen'
__date__ = '01/12/2023'
__version__ = '1.0'
__last_changed__ = '18/12/2023'
class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type or exc_val or exc_tb:  # If an error occurred, rollback any changes
                self.conn.rollback()
            else:  # Otherwise, commit any changes
                self.conn.commit()
            self.conn.close()

    # def create_table(self):
    #     print("Hello, World!-------------------------------------------------------")
    #
    #     with self as conn:
    #         conn.execute('''
    #         CREATE TABLE IF NOT EXISTS TubeQrcode (
    #             qr_code INTEGER PRIMARY KEY,
    #             datum DATE
    #         )
    #
    #         ''')


    def create_plasmid_table(self):
        with self as conn:
            conn.execute('''
            CREATE TABLE IF NOT EXISTS Plasmid (
                plasmid_nr TEXT PRIMARY KEY,
                antibiotika TEXT,
                vektor TEXT,
                "insert" TEXT,
                quelle TEXT,
                sequenz_nr TEXT,
                konstruktion TEXT,
                verdau TEXT,
                bemerkung TEXT,
                farbecode TEXT
            )
            ''')

    def create_global_ids_table(self):
        with self as conn:
            conn.execute('''
            CREATE TABLE IF NOT EXISTS GlobalIDs (
                global_id INTEGER PRIMARY KEY
            )
            ''')

    def create_experiment_table(self):
        with self as conn:
            conn.execute('''
            CREATE TABLE IF NOT EXISTS Experiment (
                exp_id TEXT PRIMARY KEY,
                name TEXT,
                vorname TEXT,
                anz_tubes INTEGER,
                anz_plasmid INTEGER,
                datum DATE,
                video_id VARCHAR(255),
                anz_fehler INTEGER,
                bemerkung TEXT
            )
            ''')


    def create_tubes_table(self):
        with self as conn:
            conn.execute('''
            CREATE TABLE IF NOT EXISTS Tubes (
                qr_code INTEGER PRIMARY KEY,
                probe_nr INTEGER,
                exp_id TEXT,
                plasmid_nr TEXT,
                FOREIGN KEY (exp_id) REFERENCES Experiment(exp_id),
                FOREIGN KEY (plasmid_nr) REFERENCES Plasmid(plasmid_nr)
            )
            ''')
    def create_laborant_table(self):
        with self as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS Laborant (
                    name TEXT,
                    vorname TEXT,
                    anz_exp INTEGER
                )
            ''')
            # print("Tabelle 'Laborant' wurde erstellt.")

    def create_tracking_log_table(self):
        with self as conn:
            conn.execute('''
            CREATE TABLE IF NOT EXISTS TrackingLog (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exp_id TEXT,
                probe_nr INTEGER  ,
                Startstation TEXT,
                Startzeit TEXT,  
                Zielstation TEXT,
                Zielzeit TEXT,   
                Dauer INTEGER,
                Zeitstempel TEXT
            )
            ''')


