import os
import subprocess

from PyQt6.QtCore import QThread, pyqtSignal
from main import InterprocessCommunication

class WorkerThread(QThread):
    messageSignal = pyqtSignal(str)

    def run(self):
        # Create an instance of InterprocessCommunication
        ipc = InterprocessCommunication(is_debug=True)

        while True:
            received_message = ipc.receive_message()

            if received_message == 'q':
                self.messageSignal.emit('Program Exited!')
                break

            if received_message:
                self.messageSignal.emit(received_message)

            # Simulate sending a message to the child process
            ipc.send_message("Hello from WorkerThread!")

        # Clean up and stop the child process
        ipc.send_message('q')
        ipc.stop_child_process()

if __name__ == "__main__":
    # Example usage:
    worker_thread = WorkerThread()
    worker_thread.start()
