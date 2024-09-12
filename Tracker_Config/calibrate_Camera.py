"""Kann die Kalibrierwerte der Kamera erzeugen und bietet die Möglichkeit diese zu speichern/laden und zum Entzerren
von Bildern zu benutzen. Bei Ausführung wird eine Kalibrierdatei erzeugt"""

__author__ = 'Mirko Mettendorf'
__date__ = '20/05/2023'
__version__ = '1.0'
__last_changed__ = '13/07/2023'

import os
import pathlib
from configparser import ConfigParser

import cv2
from cv2 import aruco

from Tracker_Config.path_configuration import PathConfiguration

print("Tracker_Config: "+os.getcwd())

path_config = PathConfiguration()
config_object = path_config.load_configuration()


# Lese Config Datei
# config_object.read("Tracker_Config\\tracker_config.ini")
calibConf = config_object["Calibration"]

# Parameter
IMAGES_DIR = calibConf["image_directory"]
IMAGES_FORMAT = calibConf["image_format"]
MARKER_LENGTH = float(calibConf["marker_length"])
SQUARE_LENGTH = float(calibConf["square_length"])


def save_coefficients(mtx, dist, path):
    """Speichert die Kamera Matrix und Distortion Koeffizienten ab

    Args:
        mtx: Kamera Matrix Objekt
        dist: Distortion Koeffizient Objekt
        path: Zielpfad

    """

    # schreibt Werte in Datei
    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_WRITE)
    cv_file.write('K', mtx)
    cv_file.write('D', dist)
    cv_file.release()


def load_coefficients(path):
    """Ladet die Kamera Matrix und die Distortion Koeffizienten aus Datei

    Args:
        path: Pfad der Datei
    """
    # Datei lesen
    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_READ)
    camera_matrix = cv_file.getNode('K').mat()
    dist_matrix = cv_file.getNode('D').mat()
    cv_file.release()
    return [camera_matrix, dist_matrix]


def calibrate_charuco(dirpath, image_format, marker_length, square_length):
    """Führt die Kalibrierung mithilfe von aruco aus

    Args:
        dirpath: Pfad wo die Kalbrierbilder abgelegt sind
        image_format: Dateiendung, jpg,png ...
        marker_length:  Aruco Marker Breite
        square_length: Quadrat Marker Breite

    Returns:
        Gibt alle Werte der aruco.calibrateCameraCharuco() Methode als Tupel zurücl
    """

    # aruco settings
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_1000)
    board = aruco.CharucoBoard((5, 7), square_length, marker_length, aruco_dict)
    detector = aruco.CharucoDetector(board)

    # Listen
    counter, corners_list, id_list = [], [], []

    # Läd Bilder
    img_dir = pathlib.Path(os.getcwd()+dirpath)

    # Suche den Marker in jedem Bild
    for img in img_dir.glob(f'*{image_format}'):
        print(f'using image {img}')
        image = cv2.imread(str(img))
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        charuco_corners, charuco_ids,marker_corners,marker_ids = detector.detectBoard(img_gray)

        # Wenn Marker korrekt erkannt wurden
        if len(charuco_corners)>3:
            # Füge die Felder und IDS zu den Listen hinzu
            corners_list.append(charuco_corners)
            id_list.append(charuco_ids)

    # Kalibrierung
    flags = (cv2.CALIB_RATIONAL_MODEL)
    ret,cameraMatrix, distCoeffs, rvecs, tvecs = aruco.calibrateCameraCharuco(
        charucoCorners=corners_list,
        charucoIds=id_list,
        board=board,
        imageSize=img_gray.shape,
        cameraMatrix=None,
        distCoeffs=None)
    return [ret,cameraMatrix, distCoeffs]


# Kalibrieren
if __name__ == '__main__':
    print(cv2.getBuildInformation())
    retr,cameraMatrix, distCoeffs = calibrate_charuco(
        IMAGES_DIR,
        IMAGES_FORMAT,
        MARKER_LENGTH,
        SQUARE_LENGTH
    )
    # Speichere Koeffizienten in Datei ab
    save_coefficients(cameraMatrix, distCoeffs, "calibration_charuco.yml")
