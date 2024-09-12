"""Enthält Hilfsmethoden und Klassen für den Prototyp"""

__author__ = 'Mirko Mettendorf'
__date__ = '20/05/2023'
__version__ = '1.0'
__last_changed__ = '13/07/2023'

import math
import threading
from configparser import ConfigParser

import cv2
import requests

from Tracker_Config.path_configuration import PathConfiguration

# Lese Config Datei
# config_object = ConfigParser()
# config_object.read("..\\Tracker_Config\\tracker_config.ini")
path_config = PathConfiguration()
config_object = path_config.load_configuration()
trackerConf = config_object["Tracker"]
telegramConf = config_object["Telegram"]

# Lese Tracking Config Werte aus
TUBE_ROWS = int(trackerConf["tube_rows"])
TUBE_COLUMN = int(trackerConf["tube_column"])

# Lese Telegram Config Werte aus
API_TOKEN = telegramConf["api_token"]
CHAT_ID = telegramConf["chat_id"]


class VideoCapture(cv2.VideoCapture):
    """ Überschreibt die OPENCV VideoCapture Klasse, um nur den aktuellen Frame zurückzugeben und nicht zu buffern."""

    def __init__(self, path):
        """ initialisiert die VideoCapture Instanz

        Args:
            path (): wie in cv2.VideoCapture der Kamerapfad
        """
        # öffne Kamera
        self.cap = cv2.VideoCapture(path)

        # starte eigenen Thread
        self.lock = threading.Lock()
        self.t = threading.Thread(target=self._reader)
        self.t.daemon = True
        self.t.start()

    def _reader(self):
        """ Überschreibt immer mit dem neusten Frame
        """
        while True:
            with self.lock:
                # hol neusten frame
                ret = self.cap.grab()
            if not ret:
                break

    def read(self):
        """ lese den neusten Frame

        Returns: gibt Frame zurück

        """
        with self.lock:
            flag, frame = self.cap.retrieve()
        return flag, frame


def berechne_mittelpunkt(point1, point2):
    """ Berchnet die Koordinaten des Mittelpunkts zweier Punkte

    Args:
        point1 ((x,y)): Koordinaten von Punkt 1
        point2 ((x,y)): Koordinaten von Punkt 2

    Returns: Tupel mit Koordinaten des Mittelpunkts

    """
    xm = (point1[0] + point2[0]) / 2
    ym = (point1[1] + point2[1]) / 2
    return xm, ym


def mergeIDs(liste1, liste2):
    """ Verknüpft die IDs der Tubes aus dem QR-Reader mit den IDs der Tubes des Trackers.
     Funktioniert über die relative Position der Tubes zueinander. Da diese gleich ist

    Args:
        liste1 ([(xy),id]): Liste 1 der Tubes, die aus Tupeln mit dem Mittelpunkt der Tube und der ID besteht.
        liste2 ([(xy),id]): Liste 2 der Tubes, die aus Tupeln mit dem Mittelpunkt der Tube und der ID besteht.

    Returns: Gibt Liste zurück mit Tupeln beider IDs

    """

    if len(liste1) != len(liste2):
        return []

    # Berechnet min und max Werte der Koordinaten beider Listen
    x_min1 = min(tube[0][0] for tube in liste1)
    y_min1 = min(tube[0][1] for tube in liste1)
    x_max1 = max(tube[0][0] for tube in liste1)
    y_max1 = max(tube[0][1] for tube in liste1)
    x_min2 = min(tube[0][0] for tube in liste2)
    y_min2 = min(tube[0][1] for tube in liste2)
    x_max2 = max(tube[0][0] for tube in liste2)
    y_max2 = max(tube[0][1] for tube in liste2)

    # Rückgabe Liste
    zugewiesen_liste = []





    # für alle Zeilen aus Config File nacheinander ablaufen
    for i in range(TUBE_ROWS):

        # für alle Spalten aus Config File nacheinander ablaufen
        for j in range(TUBE_COLUMN):
            # für jede Tube in Liste 1
            for tupel1 in liste1:

                # entpacke Tupel
                xy1, zahl1 = tupel1
                x1, y1 = xy1

                # Berechne Position der Tube als Spalten und Zeilen Wert. Dazu wird die Koordinate des unteren Linken
                # Tubes auf den Ursprung des Koordinatensystems gesetzt  (-ymn1,-xmin1). Das Verhältnis der Position
                #  (-ymn1,-xmin1) zu der maximalen möglichen Position wird auf die Anzahl an möglichen Reihen und
                #  Spalten aufgeteilt (y_max /(Tube_ROWS-1),x_max/(Tube_Columns-1)).
                zeile = round((y1 - y_min1) / ((y_max1 - y_min1) / (TUBE_ROWS - 1)))
                spalte = round((x1 - x_min1) / ((x_max1 - x_min1) / (TUBE_COLUMN - 1)))

                # stimmt mit aktueller Spalte und Zeile überein
                if zeile == i and spalte == j:

                    # für jede Tube in Liste 2
                    for tupel2 in liste2:

                        # entpacke Tupel
                        xy2, zahl2 = tupel2
                        x2, y2 = xy2

                        # Berechne Position der Tube als Spalten und Zeilen Wert
                        zeile2 = round((y2 - y_min2) / ((y_max2 - y_min2) / (TUBE_ROWS - 1)))
                        spalte2 = round((x2 - x_min2) / ((x_max2 - x_min2) / (TUBE_COLUMN - 1)))

                        # stimmt mit aktueller Spalte und Zeile überein
                        if zeile2 == i and spalte2 == j:
                            # Tubes sind identisch, also füge beide Ids zur Liste hinzu
                            zugewiesen_liste.append((zahl1, zahl2))
                            break

    return zugewiesen_liste


def calculate_distance(rect1, rect2):
    """ Berechnet den Abstand zweier Rechtecke.

    Args:
        rect1 (): Rechteck 1 mit Mittelpunkt x und y Koordinate und Höhe und Breite
        rect2 (): Rechteck 2 mit Mittelpunkt x und y Koordinate und Höhe und Breite

    Returns: Distanz der Rechtecke in Pixel. Bei Überschneidung wird 0 zurückgegeben

    """
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2

    distanceX = x1-x2
    distanceY = y1-y2
    width = w1+w2
    heigth = h1+h2

    if(abs(distanceX)<width):
        if(abs(distanceY)<heigth):
            print("Distanz: " + str(0))
            return 0
    distance = math.sqrt(distanceX ** 2 + distanceY ** 2)
    print("Distanz: " + str(distance))
    return distance

    '''if x1 + w1 < x2:
        distance_x = x2 - (x1 + w1)
    elif x2 + w2 < x1:
        distance_x = x1 - (x2 + w2)
    else:
        distance_x = 0

    if y1 + h1 < y2:
        distance_y = y2 - (y1 + h1)
    elif y2 + h2 < y1:
        distance_y = y1 - (y2 + h2)
    else:
        distance_y = 0

    distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
    print("Distanz: " + str(distance))
    return distance'''


def send_to_telegram(message):
    """ Methode um eine Nachricht über einen Telegram Bot zu versenden

    Args:
        message (str): Text zum Senden

    """
    apiURL = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': CHAT_ID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)


