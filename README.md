# Agile Roboticsystems: Lab Challenge

![git](https://github.com/Prof-Adrian-Mueller/Agile_Roboticsystems_Laborstrasse/assets/136337224/a3d2050a-7dae-4e77-876f-ed539fcca5f0)


Repository für die automatische Laborstraße des Agile Roboticsystems Projekt, 2023, 2024

Das System besteht aus 3 Teilprojekten:

- Die automatische Laborstraße (Bufe,Müller)
- Das automatische Entladen (Papyschew)
- Das automatische Erkennen und Tracken (Mettendorf)

## Einrichtung

Python 3.9 installieren\
Neuestes Java installieren\
Befehl "pip -r Tracker_Config/requirements.txt" zum Installieren der notwendigen Module im Terminal im Root Projektordner ausführen.\


## Automatische Laborstraße

Wird über die main.py in dem Ordner Main ausgeführt.\
Die Steuerung wird durch die doBot_Steuerung.py realisiert.\

Die Projekte Entladen und Tracking sind mit eingebunden\

## Automatisches Entladen

Befindet sich in dem Ordner Entladen\

## Tracking

Eine genaue Dokumentation findet man unter Dokumentation_Tracker.pdf\

Das Tracking besteht aus 2 Teilen.\
Dem Erkennen der Micro-QR-Codes. Dieser befindet sich in dem Ordner Erkennen.\
Und dem Tracker, der in dem Monitoring Ordner liegt.\

Die Kamera zum Erkennen der Micro-Qr-Codes muss über USB mit dem PC verbunden sein.

Die Micro-Qr-Code Erkennung wird über die microqr_reader.py ausgeführt.\
Wurde diese importiert, kann über die Methode microqr_reader() die Erkennung gestartet werden.\
Der notwendige Parameter ist die Anzahl an Tubes, die erkannt werden wollen.\

Die Erkennung läuft solange, bis die angegebene Anzahl an Tubes erkannt wurde\
Es wird eine Liste zurückgegeben, die die Ids der erkannten Tubes, sowie deren Mittelpunktkoordinate enthält  [(xy,id)]\

Weitere Informationen bitte der Dokumentation entnehmen.\

Die Kamera für den Tracker muss angeschaltet werden und der Hotspot am PC über den WLAN-Stick muss aktiviert sein.
Nach erfolgreicher Verbindung der Kamera muss ihre IP ausgelesen und in der Tracker_Config/tracker_config.ini Konfigurationsdatei eingetragen werden unter kameraIP

Der Tracker wird über die monitoring.py ausgeführt.\
Wurde diese importiert, kann über die start_tracking() der Tracker gestartet werden.\
Der notwendige Paramteter ist der Rückgabewert der Micor-Qr-Code Erkennung\

Der Tracker läuft parallel zu Laborstraße, bis es manuell beendet wird.\
Die Ergebnisse werden in dem in der Tracker_Config/tracker_config.ini angegebenen Zielordner unter dem aktuellen Datum und Uhrzeit als .csv Datei gespeichert.\

Weitere Informationen bitte der Dokumentation entnehmen.\

  ### Konfiguration

  Die Konfiguration des Trackings, sowie weitere Hilfsprogramme befinden sich in dem Tracker_Config Ordner.
  Die Bedeutung der unterschiedlichen Parameter der tracker_config.py bitte der Dokumentation entnehmen.
____

# Agile Roboticsystems Laborstrasse GUI Dashboard

This is a Dashboard Application for Agile Roboticsystems Laborstrasse, which is created using PyQt6.

## Prerequisites

Ensure the following components are installed :
- Python 3.9 or later
- pip (Python Package Installer)

## Setup

1. **Clone the repository** to your local machine using Git.

```bash
git clone https://github.com/Prof-Adrian-Mueller/Agile_Roboticsystems_Laborstrasse.git
```

2. **Navigate** into the main folder `Agile_Roboticsystems_Laborstrasse`.

```bash
cd Agile_Roboticsystems_Laborstrasse
```

3. **Create a virtual environment** in the main folder. We'll name it `venv`.

```bash
python3 -m venv venv
```

4. **Activate the virtual environment**. On Windows, use:

```bash
venv\Scripts\activate
```

On Unix or MacOS, use:

```bash
source venv/bin/activate
```

5. **Install the required Python packages**. If you have a `requirements.txt` file, you can install all required packages using:

```bash
pip install -r requirements.txt
```

## Running the Application

After setting up, you can run the application using the following command:

```bash
python -m GUI.MainWindow
```

This will start the ``Dashboard GUI`` application.




