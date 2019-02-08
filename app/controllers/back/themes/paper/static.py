from core.view import view
from os.path import splitext
from pathlib import Path
import mimetypes

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
            mime=mimetypes.guess_type(resource_url)
            ret['headers'] = [ ('Content-Type', mime[0]+'; charset=utf-8')]
            with open(resource_url, "rb") as imageFile:
                f = imageFile.read()
                b = bytearray(f)
            ret['body'] =bytes(b)
        return ret
