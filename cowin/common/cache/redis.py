from django.core.cache import cache


class RedisCache:
    def __init__(self):
        pass

    def set(self, key, value, ttl=180):
        print("Setting cache", key, value)
        print(cache.set(key, value, timeout=ttl))

    def get(self, key):
        return cache.get(key)


redis = RedisCache()