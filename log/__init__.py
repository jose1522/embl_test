import os
import json
from pathlib import Path
from logging import getLogger
from logging.config import dictConfig

conf_path = Path(__file__).parent
json_file = os.path.join(conf_path, 'logging.json')


def config_as_dict() -> dict:
    with open(json_file) as file:
        file = file.read()
    config = json.loads(file)
    return config


def create_logger(name):
    dictConfig(config_as_dict())
    return getLogger(name)
