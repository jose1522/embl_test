from os import getenv, path
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Variables:
    DB_URL = f"sqlite+pysqlite:///{path.join(Path(__file__).parent.parent, 'storage', 'embl.db')}"
    BROKER_URL = getenv("BROKER_URL", 'kafka://localhost')
    BROKER_TOPIC_PARTITIONS = getenv("BROKER_TOPIC_PARTITIONS", 1)
    VERBOSE_DB = getenv("VERBOSE_DB", "true").lower() == "true"
    UPSERT_RECORDS = getenv("UPSERT_RECORDS", "true").lower() == "true"
    REDIS_HOST = getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(getenv("REDIS_PORT", 6379))
    CACHING_SIZE = int(getenv("CACHING_SIZE", 10000))
    ENABLE_CACHING = getenv("ENABLE_CACHING", "false").lower() == "true"


variables = Variables()

if __name__ == '__main__':
    print(variables)