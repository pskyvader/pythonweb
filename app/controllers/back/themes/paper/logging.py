from core.view import view
from core.app import app

import os
from pathlib import Path
from core.functions import functions
import mimetypes
import datetime
import socket


class logging:
    def init(self):
        ret = {'body': ''}
        app.get
        theme = view.get_theme()
        resource = '/'.join(var)
        resource_url = theme + resource
        my_file = Path(resource_url)
        if not my_file.is_file():
            ret = {'error': 404}
        else:
            ret['is_file'] = True
            mime = mimetypes.guess_type(resource_url, False)[0]
            if mime == None:
                mime = 'text/plain'
            extension = mimetypes.guess_extension(mime)
            expiry_time = datetime.datetime.utcnow() + datetime.timedelta(100)
            ret['headers'] = [
                ('Content-Type', mime+'; charset=utf-8'),
                ('Expires', expiry_time.strftime("%a, %d %b %Y %H:%M:%S GMT")),
                ('Accept-encoding', 'gzip,deflate'),
                ('Content-Encoding', 'gzip')
            ]
            cache_file = theme+'cache/' + \
                str(functions.fecha_archivo(resource_url, True)) + \
                '-'+resource.replace('/', '-')
            my_file = Path(cache_file)
            if my_file.is_file():
                ret['file'] = cache_file
            else:
                from gzip import compress
                test = os.listdir(theme+'cache/')
                for item in test:
                    if 'resources' in resource and item.endswith(extension):
                        os.remove(os.path.join(theme+'cache/', item))
                    elif item.endswith(resource):
                        os.remove(os.path.join(theme+'cache/', item))
                f = open(resource_url, "rb").read()
                f = compress(f)

                file_write = open(cache_file, 'wb')
                file_write.write(f)
                file_write.close()
                ret['file'] = cache_file
        return ret
