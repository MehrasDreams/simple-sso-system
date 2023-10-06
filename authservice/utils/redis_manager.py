import asyncio
import redis
import os

REDIS_HOST = os.environ.get("REDIS_HOST", '127.0.0.1')
REDIS_PORT = os.environ.get("REDIS_PORT", '6379')
pool = redis.ConnectionPool(host=str(REDIS_HOST), port=REDIS_PORT, db=0)
redis = redis.Redis(connection_pool=pool)


class RedisManager:
    def __init__(self, redis_conf):
        self.redis = redis_conf

    def set_key(self, key, value):
        self.redis.set(key, value)

    def get_key(self, key):
        response = self.redis.get(key)
        return response

    def remove_by_key(self, key):
        get_key = self.redis.delete(key)
        return True

    def remove_all_key(self):
        for key in self.redis.scan_iter():
            self.redis.delete(key)


REDIS_MANAGER = RedisManager(redis_conf=redis)
