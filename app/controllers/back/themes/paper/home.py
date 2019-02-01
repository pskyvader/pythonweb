from core.view import view

url = ['home']
metadata = {'title': 'Home', 'modulo': 'home'}


def init(var):
    if 0 in var:
        if hasattr(home, var[0]) and callable(getattr(home, var[0])):
            fun = var[0]
            del var[0]
            ret = fun(var)
        else:
            ret = {
                'body': '',
                'status': '404 Not Found',
                'header': [
                    ('Content-Type', 'text/html; charset=utf-8'),
                    ('Content-Length', 0)
                ]
            }

            ret = []
    else:
        ret = index()
    return ret


def index():
    for i in range(10):
        view.add('hola-- '+str(i), 'hello world ááá bbbaa')
    ret = view.render()
    return ret
