from core.view import view
import os

url = ['home']
metadata = {'title': 'Home', 'modulo': 'home'}


def init(var):
    if len(var)>0:
        if hasattr(Dynamo, 'mymethod') and callable(getattr(Dynamo, 'mymethod')):
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
        ret = index()
    return ret


def index():
    ret={}
    view.add('title','index');
    ret['body'] = view.render('home')
    ret['headers'] = [('Content-Type', 'text/html; charset=utf-8')]
    return ret



def ver():
    ret={}
    view.add('title','ver');
    ret['body'] = view.render('home')
    ret['headers'] = [('Content-Type', 'text/html; charset=utf-8')]
    return ret
