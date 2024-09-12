# Notes 23.11.2023
# TODO 
- mehrfache import muss Fehlerfrei funktionieren , kein Error 
	- nach Änderung in Excel sollte Experiment aktualisiert
- Info an Benutzer wie viel neue/vorhandene Tubes

# Gui
x - Redirect von stdin, stdout, stderr zu Gui

Seiten Prinzip  für Experiment Vorbereitung

- x Experiment anlegen oder importieren - Wissam Alamareen
- Plasmid Metadaten importieren - Wissam Alamareen
- Qr codes anzeigen - Ujwal Subedi

- Plasmid Nr für qr eintragen - Wissam Alamareen
- Speichern oder update - Wissam Alamareen

Idee - Jede Experiment Vorbereitung mit exp process id zuweisen damit jeder process nochmal

# Notes 16.11.2023
## TODO 
- Importierte Daten in table view anzeigen
- Funktion Export von geänderte Daten in der Experimente Tabelle
-  Stdout/Stderr wird auf Modal Fenster angezeigt - 
- responsive layout
____

## GUI (Ujwal Subedi)
- x - Start E&T Applikation 
	- Stdin Anzahl Tubes anfrage von E&T zur GUI
	- GUI zeigt Dialog Fenster
	- input Anzahl text zurück zur E&T
- x - Modal Fenster Layout Design
- 
- x - Anstatt process zu killen, schickt GUI eine Nachricht "quit" an E&T damit es mit system.exit(0) gestoppt wird
- x - Bug Fix QR Code Generator
- x - Experiment View mit dummy daten
- x - Plasmid Metadaten View mit dummy daten
- x - Text Output auf Modal Fenster  kann mit copy button in die Ablage kopiert werden
## DatenVerwaltung (Wissam Alamareen)
- x - Experiment Template Excel Datei
- x - Experiment Daten import durch eine Excel Datei
- x - Experiment Daten zurück 
- 

# Notes 7.11.2023
- Start von der E&T Applikation von GUI - Ujwal Subedi
- Excel Datei Import Auswahl durch GUI - Ujwal Subedi
- Die Datei von dem Labor (Labor Metadaten) in Datenbank in einer Tabelle speichern - Wissam Alamareen
	- spalten von Metadaten ausgewählt - nach Absprache von 17.10
- Liste von Live View Zeile (nur Template) - Ujwal Subedi
- View für Plasmid Metadaten Tabelle, Import - Ujwal Subedi & Wissam Alamareen

# TODO
- standard Error/Output/input (stdout stderr stdin) in einem Fenster auf GUI anzeigen - Ujwal Subedi
- probeid usw von threads auslesen??
- angabe der Zahl n über GUI - E&T wird mit diesem Zahl gestartet
- live view zeigt nur n Zeilen
- QR Code Generator - als Bild generieren (plugin)
- View für Tubes Tabelle "Experiment" , Importer, Exporter am Ende des Experiments - siehe Zettel von meeting 16/11
- Experiment erstellen - update Experiment mit neuen Daten
	- ein Experiment kann mehrere Tage dauern
- Ein Prozess
	- Beim Import rechnet das System aus, welche Global Id neue ist - darauf wird die Experimente Tabelle erstellt
	1.  Benutzer importiert tabelle. Das system liest m neue Zeilen ein; GUI gibt die nächste freie QR codes aus
	2. Laborant holt sich n neue QR Codes über das GUI aus der Datenbank; n<=m 
	3. Laborant druck die Codes und klebt sie darauf
	4. Laborant trägt die Zahlen plasmidisolation(Tubes) in die Spalte global id ist gleich Qr Code
	5. benutzer druckt start -> zahl n wird zur app übermittelt
	6. Randbedingungen : 
		1. Jeder QR Code darf nur einmal verwendet werden über Lebenszeit des Systems
		2. Pro Experiment sind die Anzahl des Tubes gerade
		3. Bei Jedem Import ist ein Neue Tubes zu erwarten
	 

# Notes 17.10
- done: Poc QR code counter
- ToDo: git minis pc Transformer2023
Prio 1
- xls extern wird erweitert --> Einlesen xls, hochzählne qr, automatisch  differenz zum letzten Import
- dazu_ Tabelle "Experiment" Id, Datum, Nutzer, Plasmid, 
- Nummer QR werden generiert
- dazu GUI "Neues Experiment" vorbereiten" programmieren
- Testcase_ Simulierte Fehler im Code -> anzeigen
- Export ->QA 
- n Durchgänge
- Code, Kommentare, DB Schema, GUI Texte ok

Prio 2
_ GUI Navigatiom
a) Neues Experiment Anlegen (s. Prio 1)
b) Home: Vergangene Exp. anzeigen, LIve view - incl. Export , Tracking starten

Prio 3
- TRacking Mettendorf anbinden an die DB 

Prio 4
- intermettierend (1/s) live aktualisieren
- Fehler live in LIVE melden
- 

# Notes 10-10

;; This buffer is for text that is not saved, and for Lisp evaluation.
;; To create a file, visit it with C-x C-f and enter text in its buffer.

Historie:
-p IMST Challenger Sommer 23 Ziele: automatiserung  von laborabläufe, ohne überwachnh, kosten, warnung bei störungen, hoch konfigurierbar + low
- mettendendorf: nachfolgeprojekt
- erffassung , datenhaltung im appliltoon, live tracking
- dynmisch, aggregration , mutli-threads
- config layout, trhesholds


Datenhaltung

- plasmid: pmb_100 - non-unique
- unique: qr_code [1..100.000]
- global_id: plas,mid x qr_code  unique

- db: zähler incr. qr_code next_qr_code -> print

- Erfassung je experiment: Mettendord

- tracking_id <-> global_id


- weitere ids: vorname.name (Laborant)
- 

- offline data xcecl, einige attributr für trakcing, anderen GUI ("metadaten")
- neue daten enpflegen -> Manuell verbeben gedrucklt, easst mit der tracking id.
- bandbreite u QR

- lite: vorfeld sqllitr python
- import/export
- nicht im GUI
- datenparen

GUI
- from scratch,
- modi: liove track, import/export, serch meta-daten, ststisitik, ...
- replay
- QT x Python
- Datenhsltung wie interagieren?
- datenparen


Architektur:
- start python->
  - started erfasung und tracking
  - started QT als dritter thread in Pytjhon
 - liest async. tracking daten aus
 am Ende experiment: Auswertung <(Aggregation) in DB schreiben
QT reagiert suf user cmds



Offene Fragen
- wer kontroliert start/stop
- aktualisiierung wann, wer triggered: sockets? cyclic polling?



Ausschlüssee
- skalierung
- Bandbreite QR-Codes ost ausreichend
...

___
 Filter- und Suchfunktionen, um spezifische Daten aus der Vergangenheit schnell zu finden. 6. 
 Suche nach Meta-Daten von Experimenten:  Möglichkeit zur Suche nach spezifischen Meta-Daten im Zusammenhang mit den Experimenten.