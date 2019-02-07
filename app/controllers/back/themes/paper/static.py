from core.view import view
from pathlib import Path

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
        template_url = theme + template + "." + view.extension
        my_file = Path(template_url)
        if not my_file.is_file():

        ret = {
                'error': 404
            }

        return ret