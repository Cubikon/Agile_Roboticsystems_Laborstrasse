# STEUERZENTRALE
# Autor: David Weyer
# Version 1.6
# Änderungen: neue reqirements.txt für alle Projekte zusammen
#             DLL Ordner in Path Variable gesetzt, funkioniert nicht auf labor pc
#             Schleife funktioniert
#              magnet funktioniert
#             dobot fährt mit original api call und homing bei start

# TODO:
#       A: Ablauf für automatische Laborstraße
#       B: DLL aus Ordner zu laden funktioniert auf dem Laborpc nicht
#       C: Empfehlung Magnet über Relais und 5 Volt schalten vermutlich Port 13,
#       D: Whisker direkt ohne Breadbord

import sys
import os
 
parent_dir = os.path.normpath(os.path.join(os.getcwd(), '..'))
sys.path.insert(0,parent_dir)

import Monitoring.monitoring as monitoring

if monitoring:
    print("Success!!")

sys.path.insert(1,'./DLL')

import Erkennen.microqr_reader as erkennen
import Main.DobotDllType as dType
#import Entladen.entladen as entladen

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}


def commandDelay(api,lastIndex):
    dType.SetQueuedCmdStartExec(api)
    while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
        dType.dSleep(200)
    dType.SetQueuedCmdStopExec(api)


class SteuerungControl:
    def __init__(self):
        print("Steuerung")
    def steuerung(self):
        # api laden
        api = dType.load()
        # Verbindung aufbauen
        state = dType.ConnectDobot(api, "", 115200)[0]
        print("Connect status:",CON_STR[state])
        if state == dType.DobotConnect.DobotConnect_NoError:
            dType.SetQueuedCmdClear(api)
            #Async Motion Params Setting
            dType.SetHOMEParams(api, 250, 0, 50, 200, 0)
            dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, 0)
            dType.SetPTPCommonParams(api, 100, 100, 0)
            dType.SetPTPJumpParams(api,150,150)

            #Async Home
            dType.SetHOMECmd(api, temp = 0,)
            print(dType.GetPose(api))
            dType.dSleep(1000)
            # Loop: Solange fragen bis man eine gültige Eingabe bekommt (Anzahl der Tubes abfragen)
            invalid_input = True
            while invalid_input:
                # Abfrage: Wieviele Tubes werden bearbeitet
                print("Auf pipsen des Dobots warten")
                anzahl_tubes = int(input("Anzahl der Tubes eingeben: "))
                # Fehlerkennung: Eingabe muss eine Zahl zwischen 1 und 12 sein!
                if anzahl_tubes < 1 or anzahl_tubes > 12:
                    print("Ungültige Eingabe -> Eingabe muss eine Zahl zwischen 1 und 12 sein!")
                    continue
                # Ausgabe: Input
                else:
                    invalid_input = False
                    print("Eingabe: " + str(anzahl_tubes))





            # Code von Papyshew wird aufgerufen
            #entladen.main(anzahl_tubes)

            # EventListener = wartet auf einen Input auf Pin 14 vom DoBot-Interface
            #while dType.GetIODI(api, 14)[0]!=1:
            #   print("wait for Whisker")


            # Wenn der Input ausgelöst wird
            print("Whisker-Input detected!")

            # Code von Mettendorf wird aufgerufen
            tubes =erkennen.microqr_reader(anzahl_tubes)
            monitoring.start_tracking(tubes)
            # Rückgabe wird abgeglichen -> evtl abbruch

            # Loop: Wiederhole die Tube Entnahme (i = anzahl_tubes)
            offset_x = 0
            offset_y = 0
            for i in range(1): #TODO für mehrere Codes differenz der tubes messen
                # DoBot fährt auf Position des Tubes (Position des 1. Tubes + Offset)
                dType.SetPTPCmd(api,dType.PTPMode.PTPJUMPXYZMode,-66.8816 + offset_x,-221.5284 + offset_y,65.2446,-80,1)
                dType.SetWAITCmd(api,2000)
                dType.SetEndEffectorGripper(api, 1,  1, isQueued=1)
                dType.SetWAITCmd(api,2000)

                dType.SetPTPCmd(api,dType.PTPMode.PTPJUMPXYZMode,94.2976,238.4906,1.8375,-80)
                dType.SetWAITCmd(api,2000)
                #TODO aufschrauben
                dType.SetIOMultiplexingEx(api, 17, 1, 0)  #wichtig zu konfiguration des pins, letzter parameter is queued 0 ist wichtig
                dType.SetIODO(api,17,1,0) # 12 Volt On
                dType.dSleep(10000)
                dType.SetIODO(api, 17, 0, 0) # 12 Volt Off
                dType.SetPTPCmd(api,dType.PTPMode.PTPJUMPXYZMode,-86.8816 + offset_x,-221.5284 + offset_y,65.2446,-80)
                dType.SetEndEffectorGripper(api, 1,  0, isQueued=1)
                dType.SetWAITCmd(api,2000)
                dType.SetEndEffectorGripper(api, 0,  0, isQueued=1)

                # DoBot verrechnet offset -> geht 3 Reihen à 4 Tubes durch
                #TODO offset bestimmen
                offset_x += 40
                if i == 3 or i == 7:
                    offset_y += 20
                    offset_x = 0


            #TODO schranke entfernen

            dType.SetPTPCmd(api,dType.PTPMode.PTPJUMPXYZMode,250, 0, 50, 200,1)
                #dType.SetIODO(api,17,1,0)
                # Abfrage: Wird das letzte Tube bearbeitet -> wenn ja, wird der Blocker am Ende bewegt
                #if i == anzahl_tubes - 1:
                    #playback_file = "./MoveBlocker.playback"
                    #dobot.SetPlaybackCmd(playback_file)
                    #dobot.Playback()


            # Verbindung trennen
            dType.DisconnectDobot(api)

            while True:
                if input("Drück q zum beenden")=="q":
                    break
            # Thymio fährt weiter...
            # ENDE