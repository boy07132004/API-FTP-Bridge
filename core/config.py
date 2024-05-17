import logging
from configparser import ConfigParser


def load_config(path: str):
    _config = ConfigParser()

    try:
        with open(path, 'r') as config_file:
            _config.read_file(config_file)

    except FileNotFoundError:
        logging.error("Configuration file not found: " + path)
        raise
    except Exception as e:
        logging.error("Error reading configuration file: " + path)
        raise

    return _config
