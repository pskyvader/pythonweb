#import cgitb
#cgitb.enable()
import sys
import os
from view import view
from cgi import parse_qs

sys.path.insert(0, os.path.dirname(__file__))


def init(environ):
    url = parse_qs(environ['QUERY_STRING'])
    for i in range(10):
        view.add('hola'+str(i),'hello world')
    return view.render()