from core.view import view
from os.path import splitext
from pathlib import Path

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
            from codecs import open
            #ret['body'] = open(resource_url, "r",encoding = "ISO-8859-1").read()
            ret['body'] = open(resource_url, encoding='utf-8').read()
            file_extension = splitext(resource_url)[1][1:]
            ret['headers'] = [ ('Content-Type', 'text/'+file_extension) ]
        return ret
