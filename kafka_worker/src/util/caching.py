import redis
from conf import variables

conn = redis.Redis(host=variables.REDIS_HOST, port=variables.REDIS_PORT)


class Cache:

    def __init__(self):
        self.conn = conn

    def exists(self, key) -> bool:
        result = self.conn.get(key)
        if result:
            return True
        else:
            self.conn.set(key, 0)
            return False

    def flush(self):
        self.conn.flushall(asynchronous=True)


cache = Cache()