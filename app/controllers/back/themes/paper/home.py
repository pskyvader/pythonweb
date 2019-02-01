from core.view import view
import os


def init(var):
    h = home()
    if len(var) > 0:
        if hasattr(h, var[0]) and callable(getattr(h, var[0])):
            return False
        if var[0] in dir(os):
            fun = var[0]
            del var[0]
            ret=getattr(h(), fun)(var)
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
        view.add('title', 'index')
        ret['body'] = view.render('home')
        ret['headers'] = [('Content-Type', 'text/html; charset=utf-8')]
        return ret

    def ver(self):
        ret = {}
        view.add('title', 'ver')
        ret['body'] = view.render('home')
        ret['headers'] = [('Content-Type', 'text/html; charset=utf-8')]
        return ret
