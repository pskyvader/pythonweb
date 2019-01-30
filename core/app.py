#import cgitb
#cgitb.enable()
import sys
import os
from core.view import view
from cgi import parse_qs

def init(environ):
    data_return={}
    data_return['status']="200 OK"
    data_return['content_type']='text/html'
    data_return['url'] = parse_url(parse_qs(environ['QUERY_STRING']))

    for i in range(10):
        view.add('hola'+str(i),'hello world')

    view.add('url_data',str(parse_qs(environ['QUERY_STRING'])))
    
    data_return['response_body']=view.render()
    
    return data_return

def parse_url(url):
    url=url['url'].split('/')
    return url
