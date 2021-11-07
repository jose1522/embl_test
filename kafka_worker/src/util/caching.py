import redis
import pickle
from conf import variables


class Cache:

    def __init__(self):
        self.conn = redis.Redis(host=variables.REDIS_HOST, port=variables.REDIS_PORT)

    def exists(self, key):
        record = self.conn.get(key)
        if record:
            record = pickle.loads(record)
        return record

    def keep(self, key, value):
        value = pickle.dumps(value)
        self.conn.set(key, value)

    def flush(self):
        self.conn.flushall()


