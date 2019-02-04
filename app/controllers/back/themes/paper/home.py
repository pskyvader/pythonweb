from core.view import view
from core.functions import functions
import os


def init(var):
    h = home()
    if len(var) > 0:
        if hasattr(h, var[0]) and callable(getattr(h, var[0])):
            fun = var[0]
            del var[0]
            method=getattr(h, fun)
            ret = method(var)
        else:
            ret = {
                'error': 404,
            }
    else:
        ret = h.index()
    return ret




class home:
    url = ['home']
    metadata = {'title': 'Home', 'modulo': 'home'}

    def index(self):
        ret = {}
        url_return=functions.url_redirect(self.url)
        view.add('title', str(functions.current_url()))
        ret['body'] = view.render('home')
        ret['headers'] = [('Content-Type', 'text/html; charset=utf-8')]
        return ret

    def ver(self,var):
        ret = {}
        view.add('title', 'ver')
        ret['body'] = view.render('home')
        ret['headers'] = [('Content-Type', 'text/html; charset=utf-8')]
        return ret
