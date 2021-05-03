import redis
from django.conf import settings


class RedisCache:
    def __init__(self):
        self.client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

    def set(self, key, value, ttl=180):
        return self.client.set(key, value, ex=ttl)

    def get(self, key):
        return self.client.get(key)

    def add_to_set(self, key, *values):
        return self.client.sadd(key, *values)

    def remove_from_set(self, key, *values):
        return self.client.srem(key, *values)

    def get_members_from_set(self, key):
        return self.client.smembers(key)

    def add_key_value_to_hash(self, name, key, value):
        return self.client.hset(name, key, value)

    def get_value_from_hash(self, name, key):
        return self.client.hget(name, key)

    def delete_key_from_hash(self, name, key):
        return self.client.hdel(name, key)

    def get_all_keys_from_hash(self, name):
        return self.client.hgetall(name)

    def get_all_values_from_hash(self, name):
        return self.client.hvals(name)

    def get_all_key_values_from_hash(self, name):
        return self.client.hgetall(name)

    def key_exists_in_hash(self, name, key):
        return self.client.hexists(name, key)


redis = RedisCache()
