from os import getenv,path
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


def get_project_root() -> Path:
    return Path(__file__).parent.parent


class Variables:
    DB_URL = f"sqlite+pysqlite:///{path.join(get_project_root(),'embl.db')}"
    BROKER_URL = getenv("BROKER_URL", 'kafka://localhost')
    BROKER_TOPIC_PARTITIONS = getenv("BROKER_TOPIC_PARTITIONS", 1)
    VERBOSE_DB = False


variables = Variables()