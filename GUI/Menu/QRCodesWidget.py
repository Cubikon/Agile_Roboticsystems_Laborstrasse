import os

import qrcode
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QImage, QPalette, QColor
from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QHBoxLayout, QPushButton, QSizePolicy, QFrame

from GUI.Storage.BorgSingleton import CurrentExperimentSingleton


class QRCodesWidget(QWidget):
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.current_experiment = CurrentExperimentSingleton()
        self.experiments_qr_data = None
        self.main_window = main_window
        self.layout = QVBoxLayout(self)  # Main layout of the widget

        # Create the refresh button and add it to the layout
        # Header area
        h_layout = QHBoxLayout()
        self.header_label = QLabel('QR Overview')
        h_layout.addWidget(self.header_label)

        h_layout.addStretch(1)  # This will push the following widgets to the right
        self.refresh_btn = self.create_refresh_btn()
        h_layout.addWidget(self.refresh_btn)
        self.layout.addLayout(h_layout)

        scroll = QScrollArea(self)
        self.layout.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Disable horizontal scrolling

        frame = QFrame(scroll)
        scroll.setWidget(frame)

        # this is the main layout where data should be added
        self.outputLayout = QVBoxLayout(frame)
        # Set the background color of the frame
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor('white'))
        frame.setPalette(palette)
        frame.setAutoFillBackground(True)

    def create_refresh_btn(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/img/refresh-double.svg"), QIcon.Mode.Normal, QIcon.State.Off)

        refresh_btn = QPushButton("")
        refresh_btn.clicked.connect(self.refresh_data)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
            }
            QPushButton:hover {
                background: #eee;
            }
        """)
        refresh_btn.setToolTip("Refresh")
        refresh_btn.setIcon(icon)

        return refresh_btn

    def refresh_data(self):
        print("refresh")
        # TODO add data to the list . here load the experiment, load all the tubes of exp and show using displayQr
        try:
            self.main_window.cache_data = self.main_window.load_cache()
            if self.main_window.cache_data or (hasattr(CurrentExperimentSingleton,
                                                       'experiment_id') and self.current_experiment.experiment_id is not None):
                self.current_experiment.experiment_id = self.main_window.cache_data.experiment_id
                self.experiments_qr_data = self.main_window.ui_db.experiment_adapter.get_tubes_data_for_experiment(
                    self.current_experiment.experiment_id)
                self.populate_table()
            else:
                self.experiments_qr_data = self.main_window.cache_data.experiment_id
        except Exception as ex:
            self.main_window.removeDialogBoxContents()
            self.main_window.show_message_in_dialog(ex)

    def fill_with_test_data(self, number_of_labels):
        for i in range(number_of_labels):
            label = QLabel("QR")
            qr_code_nr = "12345"  # Example QR code number
            tube_nr = "67890"  # Example tube number
            plasmid_nr = "ABCDE"  # Example plasmid number
            img_location = "/path/to/your"
            self.displayQrCode(f"00000{i}", str(1), "PB30")

    def displayQrCode(self, qr_code, tube_nr, plasmid_nr):
        """
        Display generated QR Images and Text to respective Row.
        """
        pixmap, img_location = self.generate_qr_code(qr_code)
        if pixmap is not None:
            layout_field = QLabel()
            layout_field.setPixmap(pixmap)
            self.appendOutput(layout_field, qr_code, tube_nr, plasmid_nr, img_location)

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
            h_layout = QHBoxLayout(widget)

            qr_vertical_box = QVBoxLayout()
            qr_vertical_box.addWidget(label)
            qr_code_label = QLabel(qr_code_nr)
            qr_code_label.setObjectName("qrCodeLabel")
            qr_vertical_box.addWidget(qr_code_label)

            v_widget = QWidget()
            v_widget.setLayout(qr_vertical_box)

            probe_nr_text = QLabel(tube_nr)
            probe_nr_text.setFixedWidth(120)

            drucken, speichern = self.create_buttons(img_location)

            h_layout.addWidget(v_widget)
            h_layout.addWidget(probe_nr_text)
            h_layout.addWidget(speichern)
            h_layout.addWidget(drucken)

            self.outputLayout.addWidget(widget)
        except Exception as ex:
            print(f"Error: {ex}")

    def create_buttons(self, img_location):
        speichern = QPushButton("")
        speichern.setIcon(QIcon(QPixmap(":/icons/img/save.svg")))
        speichern.setFixedSize(30, 30)
        speichern.clicked.connect(lambda: self.save_qr_image_as_pdf(img_location))

        drucken = QPushButton("")
        drucken.setIcon(QIcon(QPixmap(":/icons/img/print.svg")))
        drucken.setFixedSize(30, 30)
        drucken.clicked.connect(lambda: self.print_qr_image(img_location))

        return drucken, speichern

    def print_qr_image(self, img_location):
        try:
            printer = QPrinter()
            image = QImage(img_location)

            if image.isNull():
                raise Exception("Failed to load image")

            painter = QPainter(printer)
            painter.drawImage(0, 0, image)
            painter.end()
        except Exception as ex:
            print(f"Error: {ex}")

    def save_qr_image_as_pdf(self, img_location):
        try:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            painter = QPainter(printer)

            pixmap = QPixmap(img_location)
            if pixmap.isNull():
                raise Exception("Failed to load pixmap")

            rect = painter.viewport()
            size = pixmap.size().scaled(rect.size(), Qt.AspectRatioMode.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(pixmap.rect())
            painter.drawPixmap(0, 0, pixmap)
            painter.end()
        except Exception as ex:
            print(f"Error: {ex}")

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

    def populate_table(self):
        print("Populate")
        if self.experiments_qr_data:
            while self.outputLayout.count():
                child = self.outputLayout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            for elem in self.experiments_qr_data:
                print(elem['qr_code'])
                self.displayQrCode(str(elem['qr_code']), str(elem['probe_nr']), str(elem['plasmid_nr']))
