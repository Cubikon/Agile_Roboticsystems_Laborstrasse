from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from PyQt6.QtWidgets import QApplication
import sys

class Communicate(QObject):
    speak = pyqtSignal(str)

class Client(QObject):
    def __init__(self):
        super().__init__()
        self.comm = Communicate()
        self.comm.speak.connect(self.listen)
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_for_messages)
        self.timer.start(1000)  # Check for new messages every second

    def send(self, msg):
        print(f"Client sent: {msg}")
        self.comm.speak.emit(msg)

    def listen(self, msg):
        print(f"Client received: {msg}")

    def check_for_messages(self):
        print("Check")
        # Add code here to check for new messages from the server

if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = Client()
    client.send("Hello, Server from Client!")
    sys.exit(app.exec())
