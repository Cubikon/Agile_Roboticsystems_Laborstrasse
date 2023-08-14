""" Beinhaltet den Tracker, das Lesen der notwendigen Konfigwerte und die Klassen für die Tube, Station und das Log"""

""" Inhaltsverzeichnis:

    Konfiguration 34-79
    Station Klasse 87-105
    TrackingLogEntry Klasse 110-148
    Tube Klasse 152-170
    Tracker 176-470
    Start_Tracker 476-484
        
    
"""

__author__ = 'Mirko Mettendorf'
__date__ = '20/05/2023'
__version__ = '1.0'
__last_changed__ = '13/07/2023'

import math
import os
import threading
from threading import Thread
import ast

import cv2
import pyboof as pb
from configparser import ConfigParser
import requests
import datetime
import csv
from PIL import Image

import supervision as sv
from supervision import VideoSink, VideoInfo
from ultralytics import YOLO

import Tracker_Config.calibrate_Camera as calibrate_Camera
from Tracker_Config.tracker_utils import VideoCapture, mergeIDs, calculate_distance, send_to_telegram

# Lese Config Datei
config_object = ConfigParser()
config_object.read("..\\Tracker_Config\\tracker_config.ini")
cameraConf = config_object["Camera"]
trackerConf = config_object["Tracker"]
telegramConf = config_object["Telegram"]

# Lese Camera Ips aus der Config Datei und fügt sie in die URLS des Videostreams ein
RTSP_URL = 'rtsp://admin:admin@' + cameraConf["cameraIp"] + ':554/11'

# Lese Tracking Config Werte aus
STATION_NAMES = ast.literal_eval(trackerConf["station_names"])
MOVING_STATIONS = ast.literal_eval(trackerConf["moving_station_names"])
MOVING_STATIONS_DISTANCE_LIMIT = int(trackerConf["moving_stations_distance_limit"])
ERROR_WAIT_TIME = int(trackerConf["error_wait_time"])
STATION_LENGTH = int(trackerConf["length_station1"])
TRACKING_WEIGHTS_PATH = trackerConf["tracker_weights_path"]
TRACKING_FOLDER = trackerConf["zielpfad_log"]
# Erzeuge Ordner
DIRECTORY = TRACKING_FOLDER + "\\tracking_" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
TARGET_VIDEO_PATH = DIRECTORY + "\\video.mkv"
os.makedirs(DIRECTORY)

# Einstellung um rtsp stream zu lesen
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'

# MicroQRCode Config
config = pb.ConfigMicroQrCode()
config.version = 1
config.maxIterations = 10
config.maximumSizeFraction = 0.8
config.minimumSizeFraction = 0.01

# Settings für zu speicherndes Video
videoinfo = VideoInfo(1920, 1080, 30)

# Bounding_Box settings
box_annotator = sv.BoxAnnotator(
    thickness=2,
    text_thickness=1,
    text_scale=0.5
)

# Tracker Startzeit
Tracker_Start_Time = None


class Station:
    """ Bildet die unterschiedlichen Stationen der Laborstraße ab"""

    def __init__(self, name, coords, trackingID, stationID):
        """ Erzeugt ein Station Objekt

        Args:
            name (str): Stationen name
            coords ((xywh)): Koordinaten der Bounding Box in x,y Koordinate und w Breite und h höhe
            trackingID (int): ID des Trackers
            stationID (int): Index aus der Liste an Stationen in der Config File.
        """
        self.name = name
        self.coords = coords
        self.startCoords = coords
        self.trackingID = trackingID
        self.stationID = stationID
        self.tubes = []
        self.moving_names = None
        self.moving_index = 0


class TrackingLogEntry:
    """ Bildet die Logeinträge ab, für die CSV Datei

    """

    def __init__(self, tubeID, trackingID):
        """ Erzeugt ein TrackingLogEntry Objekt

        Args:
            tubeID (int): ID aus QR-Code Reader
            trackingID (int): Id des Trackers
        """
        self.tubeID = tubeID
        self.trackingID = trackingID
        self.startStation = None
        self.startStationTime = None
        self.endStation = None
        self.endStationTime = None
        self.videoTimestamp
        self.duration

    @property
    def duration(self):
        """ Getter der immer die Dauer zwischen Start und Ziel Station zurückgibt

        Returns: Dauer in Sekunden

        """
        if self.startStationTime is not None and self.endStationTime is not None:
            return (self.endStationTime - self.startStationTime).total_seconds()

    @property
    def videoTimestamp(self):
        """ Getter der immer den Timestamp des TrackingLogEntry für das Video zurückgibt

        Returns: Timestamp des Videos in Sekunden

        """
        if self.startStationTime is not None and Tracker_Start_Time is not None:
            return (self.startStationTime - Tracker_Start_Time).total_seconds()


class Tube:
    """
    Bildet Tube Objekt ab
    """

    def __init__(self, tubeID, trackingID):
        """

        Args:
            tubeID (int): ID aus QR-Code Reader
            trackingID (int): Id des Trackers
        """
        self.tubeID = tubeID
        self.trackingID = trackingID
        self.lastStation = STATION_NAMES[0]
        self.lastStationTime = datetime.datetime.now()
        self.leftStation = False
        self.nextStation = STATION_NAMES[0]
        self.nextStationDistance = None


def tracker(tube_ids):
    """ Ausführung des BOTSort-Trackers und Verwaltung aller Tubes, mit Überwachung und dem Schreiben von Logeinträgen

    Args:
        tube_ids ([(count,tube_ids)]): Liste mti den Tupeln aus dem QR-Code Scanner

    """

    # Listen für Logeinträge
    log = []
    live_tracking = []

    # Lade Yolo Weights
    model = YOLO(os.getcwd() + TRACKING_WEIGHTS_PATH)

    # Lade Kalibrierdaten
    mtx, dist = calibrate_Camera.load_coefficients('..\\Tracker_Config\\calibration_charuco.yml')

    # Bereite Kamera vor
    # cap = VideoCapture(RTSP_URL)
    cap = cv2.VideoCapture("C:\\Users\\Fujitsu\\Documents\\20230809_121620.mp4")

    # Berechne Kameramatrix mit Kalibrierdaten
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (3840, 2160), 0, (3840, 2160))
    mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (3840, 2160), 5)

    # flag für Start
    start = True

    # Listen mit Stationen und temporären tubes
    stations = []
    tubes_tracker_temp = []

    # setze globale Variable der Startzeit
    global Tracker_Start_Time
    Tracker_Start_Time = datetime.datetime.now()

    headerLog = ['tubeID', 'startStation',
                 'startStationTime',
                 'endStation',
                 'endStationTime', 'duration',
                 'videoTimestamp']
    headerLogDetail = ['tubeID', 'lastStation', 'leftStation',
                       'nextStation', 'nextStationDistance']

    frameIndex = 0

    video = cv2.VideoWriter(os.getcwd() + '\\' + TARGET_VIDEO_PATH,
                            cv2.VideoWriter.fourcc(*'X264'),
                            4, (3840, 2160))

    cv2.namedWindow("Monitoring", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Monitoring", 1920, 1080)

    # zum Speichern der Log.csv Datei
    with open(DIRECTORY + '\\log.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headerLog)
        # zum Speichern der log_detail.csv Datei
        with open(DIRECTORY + '\\log_detail.csv', 'w', newline='') as f2:
            writer2 = csv.writer(f2)
            writer2.writerow(headerLogDetail)
            # für jeden Frame
            while True:
                if (cv2.waitKey(1) % 0xFF) == ord('s'):
                    print("beende Monitoring Thread")
                    break

                # jeden xten Frame lesen
                for i in range(1):
                    # lese frame
                    flag, img = cap.read()

                # überspringen, wenn kein frame vorhanden
                if img is None:
                    # neue Verbindung versuchen
                    # cap = VideoCapture(RTSP_URL)
                    continue

                # entzerre frame mit Kameramatrix
                dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
                x, y, w, h = roi
                dst = dst[y:y + h, x:x + w]

                test = 0

                # Tracking für den aktuellen Frame
                track = model.track(source=dst, conf=0.3, iou=0.8, tracker="botsort.yaml", stream=False
                                    , save_txt=True, show=False,
                                    device='cpu', save=True,
                                    persist=True)  # bei vorhandener Nvidia Grafikkarte device auf 0 setzen
                # generator to list
                for results in track:
                    # für jedes erkannte Objekt des Trackers in dem aktuellen Frame
                    for result in results:
                        test += 1
                        print("Result: " + str(test))
                        # Detektion Objekt des aktuellen results
                        detections = sv.Detections.from_yolov8(result)
                        print(model.model.names[detections.class_id[0]])
                        # Id des Objekts erkannt
                        if result.boxes.id is not None:

                            # speichern der Id
                            detections.tracker_id = result.boxes.id.cpu().numpy().astype(int)

                            # im ersten Frame werden die tracking ids zwischengespeichert und die station Objekte
                            # erzeugt, da Tube Objekte erst nach dem Erkennen aller Tubes Objekte und der Verknüpfung
                            # mit den QR-Code IDs erzeugt werden können.
                            if start:
                                # erkanntes Objekt ist tube
                                if model.model.names[detections.class_id[0]] == "Tube":

                                    # zwischenspeichern der Koordinaten und ID
                                    tubes_tracker_temp.append(
                                        ((result.boxes.xywh.tolist()[0][0], result.boxes.xywh.tolist()[0][1]),
                                         detections.tracker_id[0]))
                                # erkanntes Objekt ist Station
                                else:

                                    name = model.model.names[detections.class_id[0]]
                                    if name in STATION_NAMES:
                                        # index der Station aus der Configlist
                                        index = STATION_NAMES.index(name)

                                        # erzeuge Station Objekt
                                        station = Station(name, result.boxes.xywh.tolist()[0], detections.tracker_id[0],
                                                          index)

                                        # aktuelle Station ist eine bewegliche Station mit Unternamen
                                        if MOVING_STATIONS[index] is not None:
                                            # Erster Name der beweglichen Station
                                            name = MOVING_STATIONS[index][0]
                                            station.moving_names = MOVING_STATIONS[index]

                                        # füge Station in Stationsliste hinzu
                                        stations.append(station)

                            # ab zweitem frame, sind alle Tracking Objekte erzeugt
                            else:
                                # es wird geprüft ob das Tube aktuell in der Station eingetragen ist, wenn nein und
                                # es ist aber jetzt in der Station, wird der Logeintrag beendet und das Tube wird in
                                # der Station vermerkt. Es hat eine Fahrt von einer Station zur nächsten beendet. Ist
                                # es nicht in der Station, es stand aber in der Liste der Station, dann hat es soeben
                                # die Station verlassen und es wird ein neuer Logeintrag erzeugt und das Tube aus der
                                # Stationliste gelöscht.

                                # erkanntes Objekt ist tube
                                if model.model.names[detections.class_id[0]] == "Tube":

                                    # für jede Station prüfen
                                    for station in stations:

                                        # Tube liegt in Station
                                        print(station.name)
                                        if calculate_distance(station.coords, result.boxes.xywh.tolist()[0]) == 0:

                                            # suche Tube in live_Tracking
                                            for tube in live_tracking:

                                                # aktuelles Objekt ist die Tube
                                                if tube.trackingID == detections.tracker_id[0]:
                                                    print("Tube " + str(tube.tubeID) +" ist in Station " + station.name )
                                                    # wenn noch nicht in Tube Liste der Station, Tube kommt neu an
                                                    # die Station
                                                    if tube not in station.tubes:


                                                        # für jeden Logeintrag
                                                        for entry in log:

                                                            # sucht richtigen Eintrag
                                                            if entry.trackingID == tube.trackingID:
                                                                # setzt Endstation und Zeit
                                                                entry.endStation = station.name
                                                                entry.endStationTime = entry.startStationTime

                                                                # löscht aus Logliste
                                                                log.remove(entry)
                                                                # schreibt zeile in CSV Datei
                                                                writer.writerow([entry.tubeID, entry.startStation,
                                                                                 entry.startStationTime,
                                                                                 entry.endStation,
                                                                                 entry.endStationTime, entry.duration,
                                                                                 entry.videoTimestamp])

                                                        # aktualisiert tube werte
                                                        tube.leftStation = False
                                                        tube.lastStationTime = datetime.datetime.now()
                                                        tube.lastStation=station.name

                                                        # fügt Tube in Station Tube Liste hinzu
                                                        station.tubes.append(tube)

                                                        # noch keine Logeinträge
                                                        if len(log)<len(live_tracking):
                                                            # für den zweiten Frame müssen die Logeinträge erstmal erzeugt werden
                                                            entry = TrackingLogEntry(tube.tubeID, tube.trackingID)
                                                            entry.startStation = station.name
                                                            entry.startStationTime = datetime.datetime.now()

                                                            # in Logliste hinzufügen
                                                            log.append(entry)

                                                            # aktualisiert tube werte
                                                            tube.lastStation = station.name
                                                            tube.leftStation = False
                                                            tube.lastStationTime = datetime.datetime.now()
                                                            tube.nextStationDistance = None
                                        # nicht in station
                                        else:
                                            print("Tube " + str(tube.tubeID) +" ist nicht in Station " + station.name )
                                            # für jede Station prüfen
                                            for tube in live_tracking:

                                                # aktuelles Objekt ist die Tube
                                                if tube.trackingID == detections.tracker_id[0]:

                                                    # wenn in Tubel Liste der Station, dann hat das Tube die Station verlassen
                                                    if tube in station.tubes:
                                                        # trackinglogentry erzeugen und mit Stationname und Zeit füllen
                                                        entry = TrackingLogEntry(tube.tubeID, tube.trackingID)
                                                        entry.startStation = station.name
                                                        entry.startStationTime = datetime.datetime.now()

                                                        # in Logliste hinzufügen
                                                        log.append(entry)

                                                        # aktualisiert tube werte
                                                        tube.lastStation = station.name
                                                        tube.leftStation = True
                                                        tube.lastStationTime = datetime.datetime.now()
                                                        tube.nextStationDistance = None

                                                        # entfernt Tube aus Station Tube Liste
                                                        station.tubes.remove(tube)

                                    # in keiner station, Abstand zur nächsten Station berechnen für jede Tube
                                    for tube in live_tracking:

                                        # aktuelles Objekt ist Tube
                                        if tube.trackingID == detections.tracker_id[0]:

                                            # Tube hat Station verlassen
                                            if tube.leftStation:

                                                # Abstand zu jeder Station berechnen
                                                for station in stations:
                                                    print(station.name)
                                                    distance = calculate_distance(result.boxes.xywh.tolist()[0], station.coords)

                                                    # in cm umrechnen
                                                    distance = distance * (STATION_LENGTH / result.boxes.xywh.tolist()[0][2] * 2)

                                                    # niedrigste Distanz in Tube abspeichern
                                                    if tube.nextStationDistance is None:
                                                        tube.nextStationDistance = distance
                                                        tube.nextStation = station.name
                                                    else:
                                                        if distance < tube.nextStationDistance:
                                                            tube.nextStationDistance = distance
                                                            tube.nextStation = station.name

                                            # schreibe log_detail.csv
                                            writer2.writerow(
                                                [tube.tubeID, tube.lastStation, tube.leftStation,
                                                 tube.nextStation, tube.nextStationDistance])

                                # objekt ist Station, Koordinaten aktualisieren
                                else:

                                    # für jede Station
                                    for station in stations:

                                        # aktuelles Objekt ist die Station
                                        if detections.tracker_id == station.trackingID:

                                            # speichere neue Koordianten der Station ab
                                            newCoords = result.boxes.xywh.tolist()[
                                                0]

                                            # Wenn bewegliche Station
                                            if station.moving_names is not None:

                                                # ändere Stationsnamen, wenn das Distanzlimit aus der Konfig
                                                # überschritten wurde
                                                #TODO wenn station wieder steht
                                                if calculate_distance(newCoords,
                                                                      station.startCoords) * (
                                                        STATION_LENGTH / newCoords[1] * 2) > \
                                                        MOVING_STATIONS_DISTANCE_LIMIT:
                                                    station.moving_index += 1
                                                    station.name = station.moving_names[station.moving_index]

                                            # überschreibe Koordinaten in Station
                                            station.coords = newCoords

                writer2.writerow("")
                # schreibe Werte in Konsole
                print(live_tracking)
                print(log)

                # schreibe Frame in Datei
                im_array = results.plot()  # plot a BGR numpy array of predictions
                cv2.imshow("Monitoring", im_array)
                video.write(im_array)
                # nach erstem Frame
                if start:

                    # Merge die Ids des QR-Codereaders und des Trackers, wenn diese übereinstimmen
                    mergedIDs = mergeIDs(tube_ids, tubes_tracker_temp)
                    if len(mergedIDs) == 0:  # zum testen !=0
                        print("not equal")
                        tubes_tracker_temp.clear()
                        stations.clear()
                    else:
                        start = False

                        # für jede Tube
                    for index in mergedIDs:
                        # erzeuge Tube Objekt und füge es in die live-tracking Liste
                        id1, id2 = index
                        live_tracking.append(Tube(id1, id2))

                # TODO testen wie lange dauert ansonsten eigener thread
                # prüfe für jede Tube
                # for tube in live_tracking:

                # Schreibe Warnung über Telegram, wenn Wait_Time überschritten
                # if ((datetime.datetime.now() - tube.lastStationTime).total_seconds() > ERROR_WAIT_TIME):
                # send_to_telegram("Tube " + str(tube.tubeID) + " ist seit " + str(
                #    ERROR_WAIT_TIME) + " Sekunden in keiner Station aufgetaucht")



            # beende auslesen der Kamera
            video.release()
            cap.release()
            # beende alle Fenster
            cv2.destroyAllWindows()


def start_tracking(tube_ids):
    """ Erzeugt einen eigenen Thread in dem die Methode tracking() läuft

    Args:
        tube_ids ([(xy),id]): Die IDs und Koordinaten aller Tubes, die getrackt werden sollen

    """
    thread = Thread(target=tracker, args=(tube_ids,))
    thread.setDaemon(True)
    thread.start()


if __name__ == '__main__':
    start_tracking([((316.5, 262.5), 3), ((179.5, 299.0), 5), ((332.5, 321.0), 4), ((193.0, 363.0), 2)])
    while True:
        if input("Drück q zum beenden") == "q":
            break
