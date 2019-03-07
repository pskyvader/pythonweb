

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
        from .functions import functions
        ruta    = functions.generar_url(url)
        current = functions.current_url()
        if (ruta != current) {
            return ""
        }

        if (null == self.cacheable_config) {
            config                 = app.getConfig()
            self.cacheable_config = (isset(config['cache']) ? config['cache'] : true)
            if (!self.cacheable_config) {
                self.cacheable = false
            }
        }

        if (app._front && self.cacheable) {
            dir  = app.get_dir(true) . 'cache/'
            name = self.file_name(url)
            if ("" != name && file_exists(dir . name)) {
                return file_get_contents(dir . name)
            } else {
                return ""
            }
        }
    }