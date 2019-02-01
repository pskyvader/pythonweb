from core.view import view

url = ['home']
metadata = {'title': 'Home', 'modulo': 'home'}


def init(var):
    if 1 in var:
        exist=hasattr(home, 'index') and callable(getattr(home, 'index'))
    else:
        
    for i in range(10):
        view.add('hola-- '+str(i), 'hello world ááá bbbaa')
    return True

def index():
    for i in range(10):
        view.add('hola-- '+str(i), 'hello world ááá bbbaa')
    ret=view.render();
    return ret