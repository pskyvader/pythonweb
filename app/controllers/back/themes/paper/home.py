from core.view import view

url = ['home']
metadata = {'title': 'Home', 'modulo': 'home'}


def init():
    for i in range(10):
        view.add('hola-- '+str(i), 'hello world ááá bbbaa')
    return True
