from .app import app

class cache:
    data             = []
    cacheable        = True
    cacheable_config = None
    @staticmethod
    def set_cache(cacheable:bool):
        cache.cacheable = cacheable
    @staticmethod
    def is_cacheable():
        return cache.cacheable
    
    @staticmethod
    def add_cache(content):
        if app.front and cache.cacheable:
            cache.data.append(content)