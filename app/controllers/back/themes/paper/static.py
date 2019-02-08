from core.view import view
from os.path import splitext
from pathlib import Path
import mimetypes
import gzip

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
            mime=mimetypes.guess_type(resource_url)[0]
            ret['headers'] = [ ('Content-Type', mime+'; charset=utf-8'),('Accept-encoding', 'gzip,deflate'),('Content-Encoding','gzip')]
            with open(resource_url, "rb") as file:
                f = file.read()
                b = bytearray(f)
            ret['body'] =gzip.compress(bytes(b))
        return ret
