from core.view import view
import os


def init():
    h = home()
    h.init()


class home:
    url = ['home']
    metadata = {'title': 'Home', 'modulo': 'home'}

    def init(self, var):
        if len(var) > 0:
            if hasattr(self.__class__, var[0]) and callable(getattr(self.__class__, var[0])):
                return False
            if var[0] in dir(os):
                fun = var[0]
                del var[0]
                ret = fun(var)
            else:
                ret = {
                    'error': 404,
                }
        else:
            ret = self.index()
        return ret

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
