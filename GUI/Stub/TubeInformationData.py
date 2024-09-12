class TubeInformationData:
    def __init__(self, qrCodeNr: str, experiment_id: str, plasmid_nr: str, tube_id: str):
        """
        Initialize the TubeInformation object with the given parameters.
        :param qrCodeNr: A string representing the QR code number.
        :param experiment_id: A string representing the experiment ID.
        :param plasmid_nr: A string representing the plasmid number.
        :param tube_id: A string representing the tube ID.
        """
        pass

    def display_info(self) -> None:
        """
        Display the tube information.
        """
        pass

    def update_qrCodeNr(self, new_qrCodeNr: str) -> None:
        """
        Update the QR code number.
        :param new_qrCodeNr: The new QR code number to be set.
        """
        pass

    def update_experiment_id(self, new_experiment_id: str) -> None:
        """
        Update the experiment ID.
        :param new_experiment_id: The new experiment ID to be set.
        """
        pass

    def update_plasmid_nr(self, new_plasmid_nr: str) -> None:
        """
        Update the plasmid number.
        :param new_plasmid_nr: The new plasmid number to be set.
        """
        pass

    def update_tube_id(self, new_tube_id: str) -> None:
        """
        Update the tube ID.
        :param new_tube_id: The new tube ID to be set.
        """
        pass

# Example usage (when the methods are fully implemented):
# tube = TubeInformation("12345", "exp001", "plasmid123", "tube42")
# tube.display_info()
# tube.update_qrCodeNr("54321")
# tube.display_info()
