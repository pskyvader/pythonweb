#import cgitb
#cgitb.enable()
import view
def init():
    view.add('hola','hello world')
    view.add('hola2','hello world')
    view.add('hola3','hello world')
    view.add('hola4','hello world')
    return view.render()