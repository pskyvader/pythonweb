from core.view import view
import os
from pathlib import Path
from core.functions import functions
import mimetypes
import datetime


def init(var):
    h = static()
    if 0 in var:
        del var[0]
    ret = h.index(var)
    return ret


class static:

    def index(self, var):
        if len(var) == 0:
            return {'error': 404}

        ret = {'body': ''}
        theme = view.get_theme()
        resource = '/'.join(var)
        resource_url = theme + resource
        my_file = Path(resource_url)
        if not my_file.is_file():
            ret = {'error': 404}
        else:
            mime = mimetypes.guess_type(resource_url,False)[0]
            print(resource_url)
            if mime==None:
                mime='text/plain'
                print('text',resource_url)
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
                file_read=open(cache_file, "rb")
                ret['body'] = file_read.read()
                file_read.close()
            else:
                import gzip
                test = os.listdir(theme+'cache/')
                for item in test:
                    if 'resources' in resource and item.endswith(extension):
                        os.remove(os.path.join(theme+'cache/', item))
                    elif item.endswith(resource):
                        os.remove(os.path.join(theme+'cache/', item))
                f = open(resource_url, "rb").read()
                ret['body'] = gzip.compress(f)

                file_write = open(cache_file, 'wb')
                file_write.write(ret['body'])
                file_write.close()
        return ret
