import subprocess
import sys
import time
import threading

__author__ = 'Ujwal Subedi'
__date__ = '01/12/2023'
__version__ = '1.0'
__last_changed__ = '01/12/2023'


class InterprocessCommunication:
    """
    Process to be run by GUI. Could Send and Receive Message to GUI.
    """
    def __init__(self, is_debug=False):
        self.is_debug = is_debug

    def receive_message(self):
        line = sys.stdin.readline().strip()
        print(f"Received: {line}\n")
        return line

    def run_child_process(self):
        if self.is_debug:
            print("INPUT ANZAHL_TUBES\n")

            while True:
                received_message = self.receive_message()
                print(received_message)
                if received_message == 'exit':
                    print('Child process Exited!')
                    sys.exit(0)

    def run(self):
        if self.is_debug:
            print("E&T Started! \n Type 'exit' to stop the process.")

            # Start the child process in a separate thread
            child_thread = threading.Thread(target=self.run_child_process)
            child_thread.start()
            child_thread.join()

        else:
            print("Starting steuerung")
            from Main.doBot_Steuerung import SteuerungControl
            steuerung = SteuerungControl()
            steuerung.steuerung()


if __name__ == "__main__":
    ipc = InterprocessCommunication()

    try:
        ipc.run()
    except KeyboardInterrupt:
        print("Interrupt received, stopping child process...")
        print('Child process Exited!')
        sys.exit(0)
