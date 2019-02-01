from core.view import view

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
    for i in range(10):
        view.add('hola-- '+str(i), 'hello world ááá bbbaa')
    ret = view.render()
    return ret
