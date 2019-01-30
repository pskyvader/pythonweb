#import cgitb
# cgitb.enable()
import sys
import os
from core.view import view
from cgi import parse_qs
import json


class app:
    config={}
    app_dir='app/'
    controller_dir=''
    url={}
    front=True
    path=''
    def init(self,environ):
        data_return = {}
        data_return['status'] = "200 OK"
        data_return['content_type'] = 'text/html; charset=utf-8'
        data_return['extra'] = self.parse_extra(parse_qs(environ['QUERY_STRING']))
        data_return['extra'] = environ
        data_return['url'] = self.parse_url(environ['PATH_INFO'])
        config=self.get_config()
        if(data_return['url'][0]==config['admin']):
            self.front=False
        
        if self.front:
            self.controller_dir='front'
        else:
            self.controller_dir='back'
        site          = environ['SERVER_NAME']
        subdirectorio = config['dir']
        https         = (config['https']) ? "https://" : "http://"
        www           = (config['www']) ? "www." : ""

        
        for i in range(5):
            view.add('hola'+str(i), 'hello world ááá bbbaa')

        view.add('url_data', str(data_return['url']))
        view.add('url_extra', str(data_return['extra']))

        data_return['response_body'] = view.render()

        return data_return

    @staticmethod
    def parse_url(url):
        url = url.lstrip('/')
        if url != '':
            url = url.split('/')
            if url[0] == 'manifest.js':
                url[0] = 'manifest'
            else:
                if url[0] == 'sw.js':
                    url[0] = 'sw'
        else:
            url = ['home']
        return url

    @staticmethod
    def parse_extra(url):
        if 'url' in url:
            del url['url']
        return url

    def get_config(self):
        if len(app.config)==0:
            with open(self.app_dir+'config/config.json') as f:
                app.config = json.load(f)
        return app.config

