import os
import sys
import subprocess
import time

from PyQt6.QtCore import QThread, pyqtSignal

class WorkerThread(QThread):
    messageSignal = pyqtSignal(str)

    def run(self):
        self.process = self.start_child_process()

        while True:
            output = self.process.stdout.readline()
            if output == '' and self.process.poll() is not None:
                break
            if output:
                self.messageSignal.emit(output.strip())

        rc = self.process.poll()

    def stop_child_process(self):
        self.send_message('exit')
        print("Stopping E&T...")
        self.process.wait()

    def send_message(self, message):
        self.process.stdin.write(message + '\n')
        self.process.stdin.flush()

    def start_child_process(self):
        script_directory = os.path.dirname(os.path.abspath("Main/main.py"))
        process = subprocess.Popen(
            ["python", "-m","main.py"], 
            cwd=script_directory, 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            bufsize=1, 
            universal_newlines=True,
            text=True
        )
        return process