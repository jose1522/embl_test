import redis
import pickle
from conf import variables


class Cache:

    def __init__(self, conn=None):
        self.conn = conn or redis.Redis(host=variables.REDIS_HOST, port=variables.REDIS_PORT)

    def exists(self, key):
        record = self.conn.get(key)
        if record:
            record = pickle.loads(record)
        return record

    def keep(self, key, value):
        try:
            value = pickle.dumps(value)
            self.conn.set(key, value)
        except AttributeError as e:
            raise AttributeError(f"Can't pickle object {value}: {str(e)}")

    def flush(self):
        self.conn.flushall()


