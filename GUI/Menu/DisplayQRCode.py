import os
import qrcode
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog

from GUI.Custom.CustomDialog import ContentType
from GUI.Navigation import Ui_MainWindow
from PyQt6.QtGui import QPixmap, QIcon, QPainter, QImage
from PyQt6.QtCore import QProcess
from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QApplication, QSizePolicy, QScrollArea, QFrame
from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QLabel, QLineEdit
from PyQt6.QtCore import Qt
from GUI.Navigation import Ui_MainWindow

__author__ = 'Ujwal Subedi'
__date__ = '01/12/2023'
__version__ = '1.0'
__last_changed__ = '01/12/2023'

from GUI.Storage.BorgSingleton import TubesSingleton


class DisplayQRCode(QWidget):

    def __init__(self, ui: Ui_MainWindow, main_window):
        """
        Generates Image of a QR Code and shows in a Row List View.

        Args:
            ui: Ui_MainWindow object initialized in main window
            main_window: Default main window object
        """
        super().__init__()
        self.ui = ui
        self.main_window = main_window
        self.tubes_information = TubesSingleton()
        scroll = QScrollArea(self)
        self.ui.qr_code_list_content.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        frame = QFrame(scroll)
        scroll.setWidget(frame)
        self.outputLayout = QVBoxLayout(frame)

    def displayQrCode(self, qr_code):
        """
        Display generated QR Images and Text to respective Row.
        """
        pixmap, img_location = self.generate_qr_code(qr_code)
        if pixmap is not None:
            layout_field = QLabel()
            layout_field.setPixmap(pixmap)
            self.appendOutput(layout_field, qr_code, "tube_nr", "plasmid_nr", img_location)

    def generate_qr_code(self, number):
        """
        Generate QR Image and send back for respective
        """
        # Check if the number is 6 digits
        if len(number) == 6 and number.isdigit():
            # Generate the QR code
            img = qrcode.make(number)

            # Create the directory if it doesn't exist
            if not os.path.exists("QRCodeImages"):
                os.makedirs("QRCodeImages")
            img_location = f"QRCodeImages/qrcode{number}.png"
            img.save(img_location)
            pixmap = QPixmap(f"QRCodeImages/qrcode{number}.png")
            pixmap_resized = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
            return pixmap_resized, img_location
        else:
            print("Invalid number. Please enter a 6-digit number.")
            return None

    def appendOutput(self, label: QLabel, qr_code_nr, tube_nr, plasmid_nr, img_location):
        try:
            widget = QWidget()
            widget.setObjectName("displayQrCode")
            self.outputLayout.addWidget(widget)
            drucken, speichern = self.buttons_initialize(img_location)
            probe_nr_text = QLabel(str(tube_nr))
            probe_nr_text.setFixedWidth(120)
            qrCodeLabel = QLabel()
            qrCodeLabel.setObjectName("qrCodeLabel")
            qrCodeLabel.setText(qr_code_nr)
            h_layout = QHBoxLayout(widget)
            qrVerticalBox = QVBoxLayout()
            qrVerticalBox.addWidget(label)
            qrVerticalBox.addWidget(qrCodeLabel)
            # Create a QWidget and set the QVBoxLayout on it
            v_widget = QWidget()
            v_widget.setLayout(qrVerticalBox)
            # Add the QWidget to the QHBoxLayout
            h_layout.addWidget(v_widget)
            h_layout.addWidget(probe_nr_text)
            h_layout.addWidget(speichern)
            h_layout.addWidget(drucken)
        except Exception as ex:
            self.show_message_in_dialog(ex)

    def show_message_in_dialog(self, display_msg):
        self.main_window.dialogBoxContents.append(
            self.main_window.dialog.addContent(f"{display_msg}", ContentType.OUTPUT))
        self.main_window.dialog.show()

    def buttons_initialize(self, img_location):
        # Create the buttons and line edit
        speichern = QPushButton("")
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(":/icons/img/save.svg"), QIcon.Mode.Normal, QIcon.State.Off)
        speichern.setIcon(icon1)
        speichern.setObjectName("functional_buttons")
        speichern.setFixedHeight(30)
        speichern.setFixedWidth(30)
        speichern.clicked.connect(lambda: self.save_qr_image_as_pdf(img_location))

        icon2 = QIcon()
        drucken = QPushButton("")
        icon2.addPixmap(QPixmap(":/icons/img/print.svg"), QIcon.Mode.Normal, QIcon.State.Off)
        drucken.setIcon(icon2)
        drucken.setObjectName("functional_buttons")
        drucken.setFixedHeight(30)
        drucken.setFixedWidth(30)
        drucken.clicked.connect(lambda: self.print_qr_image(img_location))
        return drucken, speichern

    def print_qr_image(self, img_location):
        try:
            # Create a QPrinter object
            printer = QPrinter()

            # Load the image file
            image = QImage()
            image.load(img_location)

            # Create a QPainter object
            painter = QPainter()

            # Begin painting onto the printer
            painter.begin(printer)

            # Draw the image onto the printer
            painter.drawImage(0, 0, image)

            # End painting
            painter.end()
        except Exception as ex:
            print(ex)

    def save_qr_image_as_pdf(self, pixmap):
        # Create a QPrinter object
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)

        # Create a QPainter object and begin painting on the printer
        painter = QPainter(printer)

        # Draw the QPixmap on the printer
        rect = painter.viewport()
        size = pixmap.size()
        size.scale(rect.size(), Qt.AspectRatioMode.KeepAspectRatio)
        painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
        painter.setWindow(pixmap.rect())
        painter.drawPixmap(0, 0, pixmap)

        # End painting
        painter.end()
        # os.system(f"lp -o fit-to-page {file_path}")
