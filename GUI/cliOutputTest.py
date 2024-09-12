from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog, QApplication
from PyQt6.QtGui import QPixmap
import qrcode

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a QVBoxLayout
        layout = QVBoxLayout()

        # Create a QLabel to display the QR code
        self.label = QLabel()
        layout.addWidget(self.label)

        # Create a QPushButton to open the file dialog
        button = QPushButton("Generate QR Code")
        button.clicked.connect(self.generate_qr_code)
        layout.addWidget(button)

        # Create a QWidget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def generate_qr_code(self):
        number = '000001'
        # Check if the number is 6 digits
        if len(number) == 6 and number.isdigit():
            # Generate the QR code
            img = qrcode.make(number)

            img.save("qrcode.png")
            pixmap = QPixmap("qrcode.png")
            self.label.setPixmap(pixmap)


import sys

def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
