
import pandas as pd
from sqlite3 import Date
from Control.ExcelImporter import ExcelImporter
from DBUIAdapter import DBUIAdapter
  



ui_db = DBUIAdapter()
# SEITE 1
# diese Methode wird aufgerufen bei Experiment hinzufügen 
# die Methode erwartet name und nachname von laborant, anzahl der Plasmidnr, anzahl der Tubes und Datum der erstellung des Experiments
# ui_db.adapter.add_experiment("max", "Mustermann", 5,32, '2023-10-22')

# SEITE 2
# Tubes zu dem Experiment hinzufügen
# probe_nr_list = [1, 2, 3, 4, 5]
# # # probe_nr_list = [6,7]
# # # #  probe_nr_list2 = [8,9]

# ui_db.adapter.insert_tubes(probe_nr_list, 'max1', 'PHB 371 ')

# SEITE 3

# Return all Tubes für eine Bestimmte Experimet 
# tubes_for_exp = ui_db.adapter.get_tubes_by_exp_id("max1")
# for tube in tubes_for_exp:
#     print(tube)

# Diese methode erwartet exp_id und dann liefert daten von  Expriment zurück
print(ui_db.adapter.get_experiment_by_id("max1"))

# Methode insert_tube
# ui_db.adapter.insert_tube('000006',6,'maxi1','PHB 377')

# ----------------------------------------------





# # Aufruf der Methode mit der Liste und den einzelnen Werten für exp_id und plasmid_nr
# ui_db.adapter.insert_tubes(probe_nr_list, 'maxi1', 'PHB 377')


# all_tubes = ui_db.adapter.get_all_tubes()

#     # Drucken Sie die Ergebnisse
# for tube in all_tubes:
#         print(tube)
# ________________________________

# return Experiments daten

# print(ui_db.adapter.get_experiment_count_for_laborant("max"))
# print(ui_db.adapter.get_laborant_count())
# ui_db.adapter.add_experiment(2, "Max", "Mustermann", 5, '2023-10-22')
# all_experiments=ui_db.adapter.get_experiments()
# for experiment in all_experiments:
#     print(f"Experiment ID: {experiment.exp_id}, Name: {experiment.name}, Vorname: {experiment.vorname}, Anzahl Tubes: {experiment.anz_tubes},anzahl Plasmid:{experiment.anz_plasmid} Datum: {experiment.datum}")
#  ________________________________________
# ui_db.adapter.add_laborant("maxi","sch")
# ++++++++++++++++++++++++++++++++++++++++++
# ui_db.create_qr_code(5)
# ui_db.adapter.drop_table_tube_qrcode()
# # Select all data
# ui_db.adapter.select_all_from_tubeqrcode()
# Abrufen der ersten 5 QR-Codes
# first_five_qr_codes = ui_db.adapter.get_next_qr_codes(5)
# print("Erste 5 QR-Codes:", first_five_qr_codes)

# # Abrufen der nächsten 4 QR-Codes
# next_four_qr_codes = ui_db.adapter.get_next_qr_codes(4)
# print("Nächste 4 QR-Codes:", next_four_qr_codes)
# ui_db.adapter.check_qr_code_count(10)
# ++++++++++++++++++++++++++++++++++++++++++++

# file_path = 'D:\\Bachelorarbeit\\Plasmid_l.xlsx'



    
#     # Instanz der Klasse erstellen
# importer = TubeMetaDatenImporter(file_path)
    
#     # Methode zum Importieren und Ausgeben der Daten aufrufen
# importer.import_data()



# df = pd.read_excel('D:\\Bachelorarbeit\\Plasmid_l.xlsx', engine='openpyxl')
# print(df)

# file_path = 'D:\\Bachelorarbeit\\Plasmid_l.xlsx'
# importer = ExcelImporter(file_path)
# ui_db.db.create_plasmid_table()

# ++++++++++++++++++++++++++++++++++

# Metadaten

# ui_db.insert_metadaten()
# ui_db.adapter.select_all_from_plasmid()

# +++++++++++++++++++++++++++++++++

# importer.import_data()

# ui_db.insert_experiment_data()
# # ui_db.delete_all_experiment()
# all_experiments = ui_db.adapter.get_all_experiments()
    # Verarbeiten oder anzeigen Sie die Experimente
# for experiment in all_experiments:
#         print("_______________________________Returned___________________________")
#         print(f"Experiment ID: {experiment.exp_id}, Name: {experiment.name}, Vorname: {experiment.vorname}, Anzahl Tubes: {experiment.anz_tubes}, Video ID: {experiment.video_id}, Datum: {experiment.datum}, Anzahl Fehler: {experiment.anz_fehler}, Bemerkung: {experiment.bemerkung}")





