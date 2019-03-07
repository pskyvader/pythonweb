

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
        from .app import app
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
            folder  = app.get_dir(True) + 'cache/'
            name = cache.file_name(url)
            my_file = Path(folder+name)
            if my_file.is_file():
                return my_file
        
        return ""


    @staticmethod
    def save_cache(url:list):
        from .app import app
        from .functions import functions
        from os import W_OK
        from os import access
        ruta    = functions.generar_url(url)
        current = functions.current_url()
        if ruta == current and app.front and cache.cacheable:
            folder = app.get_dir(True) + 'cache/'
            if access(folder, W_OK):
                name = cache.file_name(url)
                if name!='':
                    f = open(resource_url, "rb").read()
                f = compress(f)

                file_write = open(cache_file, 'wb')
                file_write.write(f)
                file_write.close()

                    file_put_contents(folder . name, implode('', cache.data))
                    

    @staticmethod
    def file_name(url:list)
    {
        if (!isset(url['url']):
            return ""
        }

        name = str_replace('/', '-', url['url'])
        unset(url['url'])
        n = explode('.', name, 2)
        if (isset(n[1]):
            return ""
        }
        foreach (url as key => u:
            n = "__" . key . "-" . u
            n = functions.url_amigable(n)
            name .= n
        }
        post = _POST
        if (isset(post['ajax']):
            name .= '__ajax'
            unset(post['ajax'])
        }
        if (count(post) > 0:
            return ""
        }

        return name
    }