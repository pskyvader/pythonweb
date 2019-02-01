from core.view import view
import os

url = ['home']
metadata = {'title': 'Home', 'modulo': 'home'}


def init(var):
    if 0 in var:
        if var[0] in dir(os):
            fun = var[0]
            del var[0]
            ret = fun(var)
        else:
            ret = {
                'error': 404,
            }
    else:
        ret = index()
    return ret


def index():
    ret={}
    for i in range(10):
        view.add('hola-- '+str(i), 'hello ááá bbbaa')
    ret['body'] = view.render('home')
    ret['headers'] = [('Content-Type', 'text/html; charset=utf-8')]
    return ret
