

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
        from .app import app
        if app.front and cache.cacheable:
            cache.data.append(content)


    @staticmethod
    def delete_cache():
        import shutil
        direrctory        = app.get_dir(True) + 'cache/'
        shutil.rmtree(direrctory)
        

    @staticmethod
    def get_cache(url:list):
        from .app import app
        from .functions import functions
        from pathlib import Path
        ruta    = functions.generar_url(url)
        current = functions.current_url()
        if ruta != current:
            return ""
        

        if cache.cacheable_config==None:
            config                 = app.get_config()
            cache.cacheable_config = config['cache'] if 'cache' in config else True
            if not cache.cacheable_config:
                cache.cacheable = False
                

        if app.front and cache.cacheable:
            directory  = app.get_dir(True) + 'cache/'
            name = cache.file_name(url)
            my_file = Path(name)
            if my_file.is_file():
                return my_file
        
        return ""