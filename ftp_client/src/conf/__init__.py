from os import getenv, path
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Variables:
    BROKER_URL = getenv("BROKER_URL", 'kafka://localhost')


variables = Variables()