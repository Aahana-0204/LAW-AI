import hashlib
from cachetools import LRUCache

_cache = LRUCache(maxsize=100)


def get_cached(query: str):
    key = hashlib.md5(query.lower().strip().encode()).hexdigest()
    return _cache.get(key)


def set_cached(query: str, result: dict):
    key = hashlib.md5(query.lower().strip().encode()).hexdigest()
    _cache[key] = result


def cache_size():
    return len(_cache)
