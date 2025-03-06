from cachetools import TTLCache
from src.domain.interfaces import CacheService


class MemoryCacheService(CacheService):

    def __init__(self, maxsize: int = 100, ttl: int = 600):
        self.cache = TTLCache(maxsize=maxsize, ttl=ttl)
        self.default_ttl = ttl
    
    def get(self, key: str):
        return self.cache.get(key)
    
    def set(self, key: str, value, ttl: int = None):
        if ttl is not None:
            pass
        
        self.cache[key] = value
    
    def has(self, key: str) -> bool:
        return key in self.cache