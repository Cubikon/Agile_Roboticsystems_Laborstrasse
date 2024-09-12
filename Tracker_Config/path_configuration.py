import os
import logging
from configparser import ConfigParser

class PathConfiguration:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Config Preparation ...")

    def load_configuration(self):
        """Load and return the configuration from the ini file."""
        script_dir = os.path.dirname(__file__)
        ini_path = os.path.join(script_dir, "tracker_config.ini")
        config_object = ConfigParser()

        if not os.path.exists(ini_path):
            self.logger.error(f"Config file not found: {ini_path}")
            raise FileNotFoundError(f"Config file not found: {ini_path}")

        config_object.read(ini_path)
        # Optional: Validate the configuration here
        self.validate_configuration(config_object)
        return config_object

    def validate_configuration(self, config):
        """Validate the loaded configuration."""
        # Example validation: check for a specific section
        if not config.has_section('Calibration'):
            self.logger.error("Missing 'Calibration' section in configuration.")
            raise ValueError("Invalid configuration: Missing 'Calibration' section.")

# Example usage
path_config = PathConfiguration()
try:
    config = path_config.load_configuration()
    path_config.validate_configuration(config)
    # Use 'config' as needed
except FileNotFoundError as e:
    print(e)
    # Handle missing file
except ValueError as e:
    print(e)
    # Handle invalid configuration
