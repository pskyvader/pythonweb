

class cache:
    data = []
    cacheable = True
    cacheable_config = None
    @staticmethod
    def set_cache(cacheable: bool):
        cache.cacheable = cacheable

    @staticmethod
    def add_cache(content):
        from .app import app
        if cache.cacheable:
            cache.data.append(content)

    @staticmethod
    def delete_cache():
        import shutil
        from .app import app
        direrctory = app.get_dir(True) + 'cache/'
        shutil.rmtree(direrctory)

    @staticmethod
    def get_cache(url: list):
        from .app import app
        from .functions import functions
        from pathlib import Path
        if app.front:
            cache.cacheable = False
        ruta = functions.generar_url(url)
        current = functions.current_url()
        print('cache 1',ruta,current)
        if ruta != current:
            return ""
        print('cache 2')
        if cache.cacheable_config == None:
            print('cache 3')
            config = app.get_config()
            cache.cacheable_config = config['cache'] if 'cache' in config else True
            if not cache.cacheable_config:
                cache.cacheable = False

        if cache.cacheable:
            print('cache 4')
            folder = app.get_dir(True) + 'cache/'
            name = cache.file_name(url)
            my_file = Path(folder+name)
            if my_file.is_file():
                print(my_file)
                return my_file

        return ""

    @staticmethod
    def save_cache(url: list):
        from .app import app
        from .functions import functions
        import os
        from gzip import compress
        ruta = functions.generar_url(url)
        current = functions.current_url()
        if ruta == current and cache.cacheable:
            folder = app.get_dir(True) + 'cache/'
            if not os.path.exists(folder):
                os.makedirs(folder)
            
            if os.access(folder, os.W_OK):
                name = cache.file_name(url)
                if name != '':
                    f = ''.join(cache.data)
                    f = bytes(f, 'utf-8')
                    f = compress(f)

                    file_write = open(folder+name, 'wb')
                    file_write.write(f)
                    file_write.close()

    @staticmethod
    def file_name(url: list):
        from .app import app
        from .functions import functions
        name = '-'.join(url)
        n = name.split('.', 1)
        if len(n) > 1:
            return ""

        for key, u in app.get.items():
            ext = "__" + key + "-" + u
            ext = functions.url_amigable(ext)
            name += ext

        post = app.post.copy()
        if 'ajax' in post:
            name += '__ajax'
            del post

        if len(post) > 0:
            return ""

        return name
