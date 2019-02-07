from core.view import view
from os.path import splitext


def init(var):
    h = static()
    ret = h.index(var)
    return ret


class static:
    from pathlib import Path
    url = ['home']
    metadata = {'title': 'Home', 'modulo': 'home'}

    def index(self, var):
        ret = {'body': ''}
        theme = view.get_theme()
        resource = '/'.join(var)
        resource_url = theme + resource
        my_file = Path(resource_url)
        if not my_file.is_file() or len(var)==0:
            ret = {'error': 404}
        else:
            ret['body'] = open(resource_url, "r").read()
            file_extension = splitext(resource_url)[1][1:]
            ret['headers'] = 'Content-Type: text/'+file_extension

        return ret
