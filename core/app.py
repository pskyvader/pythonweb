#import cgitb
#cgitb.enable()
import sys
import os
from core.view import view
from cgi import parse_qs

def init(environ):
    data_return={}
    data_return['status']="200 OK"
    data_return['content_type']='text/html; charset=utf-8'
    data_return['extra'] = (parse_qs(environ['QUERY_STRING']))
    data_return['url'] = parse_url(environ['PATH_INFO'])

    for i in range(5):
        view.add('hola'+str(i),'hello world ááá bbbaa')

    view.add('url_data',str(data_return['url']))
    
    data_return['response_body']=view.render()
    
    return data_return

def parse_url(url):
    return url
    if 'url' in url:
        url=url['url'][0].split('/')
        if url[0] == 'manifest.js':
            url[0] = 'manifest'
        else:
            if url[0] == 'sw.js':
                url[0] = 'sw'
    else:
        url=['home']
    return url
