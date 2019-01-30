from core.view import view


def init():
    for i in range(10):
        view.add('hola-- '+str(i), 'hello world ááá bbbaa')
    return True
