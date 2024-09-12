import os
import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit
from PyQt6.QtCore import QThread, pyqtSignal
import multiprocessing

class ETSubprocess(QThread):
    messageSignal = pyqtSignal(str)

    def run(self):
        try:
            # Launch the E&T subprocess
            et_process = subprocess.Popen( ["python", "testclient.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            while True:
                # Check if the subprocess has terminated
                if et_process.poll() is not None:
                    break

                # Read and send signal messages from E&T to MainApplication
                signal_message = et_process.stdout.readline().strip()
                if not signal_message:
                    break

                self.messageSignal.emit(signal_message)

                # Simulate a response from MainApplication
                response_message = f"Response to signal: {signal_message}"
                et_process.stdin.write(response_message + "\n")
                et_process.stdin.flush()

            et_process.terminate()
            et_process.wait()

        except Exception as e:
            print(f"Error in E&T subprocess: {e}")


class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 300)
        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 10, 380, 200)
        self.start_button = QPushButton("Start E&T Application", self)
        self.start_button.setGeometry(10, 220, 200, 30)
        self.start_button.clicked.connect(self.start_et_subprocess)

        self.et_subprocess = None

    def start_et_subprocess(self):
        if not self.et_subprocess:
            self.et_subprocess = ETSubprocess()
            self.et_subprocess.messageSignal.connect(self.handle_et_signal)
            self.et_subprocess.start()

    def handle_et_signal(self, signal_message):
        # Handle signal messages received from E&T
        self.text_edit.append(f"Received signal from E&T: {signal_message}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApplication()
    main_window.show()
    sys.exit(app.exec())
