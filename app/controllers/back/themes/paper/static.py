from core.view import view
from pathlib import Path
from os.path import splitext

def init(var):
    h = static()
    ret = h.index(var)
    return ret



class static:
    url = ['home']
    metadata = {'title': 'Home', 'modulo': 'home'}

    def index(self,var):
        ret = {'body':''}
        theme = view.get_theme()
        resource='/'.join(var)
        resource_url = theme + resource 
        my_file = Path(resource_url)
        if not my_file.is_file():
            ret = { 'error': 404 }
        else:
            ret['body'] = open(resource_url, "r").read()
            splitext(resource_url)
            ret['headers'] = 'Content-Type: text/css'

        return ret