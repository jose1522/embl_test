from os import getenv, path
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Variables:
    DB_URL = f"sqlite+pysqlite:///{path.join(Path(__file__).parent.parent, 'storage', 'embl.db')}"
    BROKER_URL = getenv("BROKER_URL", 'kafka://localhost')
    BROKER_TOPIC_PARTITIONS = getenv("BROKER_TOPIC_PARTITIONS", 1)
    VERBOSE_DB = getenv("VERBOSE_DB", "True").lower() == "true"
    UPSERT_RECORDS = getenv("UPSERT_RECORDS", "True").lower() == "true"
    REDIS_HOST = getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(getenv("REDIS_PORT", 6379))
    COMMIT_EVERY_X_ROWS = int(getenv("COMMIT_EVERY_X_ROWS", 10000))


variables = Variables()

if __name__ == '__main__':
    print(variables)