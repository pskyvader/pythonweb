

class cache:
    data = []
    cacheable = None
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
        import os
        from .app import app
        directory = app.get_dir(True) + 'cache/'
        if os.path.exists(directory):
            shutil.rmtree(directory)

    @staticmethod
    def get_cache(url: list):
        from .app import app
        from .functions import functions
        from pathlib import Path

        if not app.front:
            cache.cacheable = False
        else:
            cache.cacheable = True

        ruta = functions.generar_url(url)
        current = functions.current_url()

        if ruta != current:
            return ""
        if cache.cacheable_config == None:
            config = app.get_config()
            cache.cacheable_config = config['cache'] if 'cache' in config else True
            if not cache.cacheable_config:
                cache.cacheable = False

        if cache.cacheable:
            folder = app.get_dir(True) + 'cache/'
            name = cache.file_name(url)
            my_file = Path(folder+name)
            if my_file.is_file():
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
