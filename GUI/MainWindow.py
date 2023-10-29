from multiprocessing import process
import subprocess
import sys
import typing
import os
from PyQt6 import QtCore
from PyQt6.QtWidgets import QGroupBox, QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTableWidgetItem, QAbstractItemView,QHeaderView, QScrollArea, QFileDialog
from PyQt6.QtGui import QIcon, QPixmap, QMouseEvent
from PyQt6.QtCore import Qt, QSize, QObject, QEvent, QTimer, QThread, QRect
import pandas as pd
from GUI.Custom.CustomDragDropWidget import DragDropWidget
from GUI.Custom.ArrayOverlay import ArrowOverlay
from GUI.Custom.CustomTableWidget import CustomTableWidget
from GUI.Custom.CustomTitleBar import CustomTitleBar
from DBService.DBUIAdapter import DBUIAdapter
from GUI.ModalDialogAdapter import ModalDialogAdapter

from GUI.Navigation import Ui_MainWindow
import GUI.resource_rc
from Main.WorkerThread import WorkerThread
from Main.main import MainClass

class RowWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.row_layout = QVBoxLayout()  # Create a QVBoxLayout

        for j in range(3):
            hbox_layout = QHBoxLayout()  # Create a QHBoxLayout for each button and label
            label = QLabel('ProbeNr')
            hbox_layout.addWidget(label)

            button = QPushButton(f'Button {j+1}')
            hbox_layout.addWidget(button)

            group_box = QGroupBox(self)  # Create a QGroupBox for each QHBoxLayout
            group_box.setStyleSheet("border:1px solid black;min-height:60px;")
            group_box.setLayout(hbox_layout)  # Set the QHBoxLayout inside the QGroupBox

            self.row_layout.addWidget(group_box)  # Add the QGroupBox to the QVBoxLayout


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        #UI Mainwindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.homeBtn.setChecked(True)
        self.setWindowTitle("Dashboard GUI")
        self.setGeometry(100, 100, 800, 600)
        self.process = any
       
        self.ui_db = DBUIAdapter()

        self.worker_thread = WorkerThread()
        self.worker_thread.messageSignal.connect(self.handle_message)

        #Custom Titlebar
        title_bar = CustomTitleBar(self)
        self.setMenuWidget(title_bar)
        # Makes the window frameless
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        #drag & drop
        self.ui.importAreaDragDrop.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint, True)
        self.ui.importAreaDragDrop = DragDropWidget(self.ui.impotPage)
        self.ui.importAreaDragDrop.setObjectName(u"dragdropwidget")
        self.ui.importAreaDragDrop.setGeometry(QRect(130, 90, 461, 261))
        self.ui.importAreaDragDrop.setStyleSheet(u"background-color:#666;")
        self.ui.chooseFileFromExplorer.clicked.connect(self.openFileDialog)

        #Custom ModalDialogBox
        # self.dialogBox = ModalDialogAdapter(self,self.ui)

        self.apply_stylesheet()

        self.ui.homeBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.homePage)))
        self.ui.statistik.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.statistikPage)))
        self.ui.importBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.impotPage)))
        self.ui.qrGenBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.qrGenPage)))
        self.ui.settingsBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.settingsPage)))

        self.ui.generateQrBtn.clicked.connect(self.add_qr_generation_info)

        self.ui.startEnTBtn.clicked.connect(self.startEnTProcess)

        

        # New code for adding buttons dynamically
        live_view_box_layout = QVBoxLayout(self.ui.scrollAreaWidgetContents_2)

        n = 20  # dynamic number of rows
        for i in range(n):
            row_widget = RowWidget()
            live_view_box_layout.addWidget(row_widget)      

        self.ui.scrollAreaWidgetContents_2.setLayout(live_view_box_layout)

    def generateLiveActionTable(self):
        self.ui.tableWidgetLiveAction.setColumnCount(4)
        # Enable smooth scrolling
        self.ui.tableWidgetLiveAction.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.ui.tableWidgetLiveAction.horizontalScrollBar().setSingleStep(15)  
        self.ui.tableWidgetLiveAction.verticalScrollBar().setSingleStep(15) 

        self.arrow_overlay = ArrowOverlay(self.ui.tableWidgetLiveAction)
        self.arrow_overlay.setGeometry(self.ui.tableWidgetLiveAction.geometry())
        self.arrow_overlay.raise_()
        self.ui.tableWidgetLiveAction.installEventFilter(self)
        # Stretch columns to fill the table width
        header = self.ui.tableWidgetLiveAction.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)   
        for row in range(32):
            rowPosition = self.ui.tableWidgetLiveAction.rowCount()
            self.ui.tableWidgetLiveAction.setRowHeight(row, 100)
            self.ui.tableWidgetLiveAction.insertRow(rowPosition)
            self.ui.tableWidgetLiveAction.setItem(rowPosition, 0, QTableWidgetItem(f"Probe #{row}"))
            start = QPushButton()
            start.setText("")           
            middle = QPushButton()
            middle.setText("")
            end = QPushButton()
            end.setText("")
            self.ui.tableWidgetLiveAction.setCellWidget(rowPosition, 1, start)
            self.ui.tableWidgetLiveAction.setCellWidget(rowPosition, 2, middle)
            self.ui.tableWidgetLiveAction.setCellWidget(rowPosition, 3, end)
        self.ui.tableWidgetLiveAction.show()
        

    def openFileDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self.ui.centralwidget, "Open File", "", "Excel Files (*.xls *.xlsx)")
        if fileName:
            print(f'Selected file: {fileName}')
            try:
                # df = pd.read_excel(fileName)
                # TODO show message in dialogbox
                print(f'Successfully imported Excel file: {fileName}')
                
            except Exception as e:
                print(f'Error occurred while importing Excel file: {fileName}\n{str(e)}')

    def eventFilter(self, source, event):
        if source == self.ui.tableWidgetLiveAction and event.type() == QEvent.Type.Resize:
            self.arrow_overlay.setGeometry(self.ui.tableWidgetLiveAction.geometry())
        return super().eventFilter(source, event)

    def startEnTProcess(self):
        #TODO Start monitoring app using python process
        
        if self.ui.startEnTBtn.text() == "Start":
            self.ui.startEnTBtn.setStyleSheet("QPushButton { background-color: red }")
            self.ui.startEnTBtn.setText("Stop")

            self.worker_thread.start()
            
              
        else:
            self.ui.startEnTBtn.setStyleSheet("QPushButton { background-color: #45a049 }")
            self.worker_thread.stop_child_process()
            print("E&T process Terminated!")
            self.ui.startEnTBtn.setText("Start")

    def handle_message(self, message):
        # TODO show this message in display box
        print(message)
        self.worker_thread.send_message("Hello from Parent!")


    def apply_stylesheet(self):
        print(os.getcwd())
        if os.path.isfile('GUI/stylesheet/stylen.qss') and os.access('GUI/stylesheet/stylen.qss', os.R_OK):
            print("File exists and is readable")
            with open('GUI/stylesheet/stylen.qss', 'r') as file:
                stylesheet = file.read()
            self.setStyleSheet(stylesheet)
        else:
            print("Stylesheet File is either missing or not readable")
            
    def add_qr_generation_info(self):
        nrOfQr = self.ui.qrNrInputBox.text()
        data = self.ui_db.create_qr_code(int(nrOfQr))
        if data is not None:
            qr_code_generated = "Folgende QR Codes sind generiert: \n"
            for qr_code in data:
                qr_code_generated += str(qr_code.qr_code) + " - "+ str(qr_code.datum)+"\n"
            self.ui.infoBoxQr.setText(f"{qr_code_generated} ")
        else:
            self.ui.infoBoxQr.setText("No QR codes were generated.")
        self.ui.qrNrInputBox.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())
