#import cgitb
#cgitb.enable()

sys.path.insert(0, os.path.dirname(__file__))
from view import view
def init():
    for i in range(10):
        view.add('hola'+str(i),'hello world')
    return view.render()