#import cgitb
# cgitb.enable()
import sys
import os
from core.view import view
from cgi import parse_qs
import json
from pathlib import Path
import importlib


class app:
    config = {}
    app_dir = 'app/'
    controller_dir = app_dir+'controllers/'
    view_dir = app_dir+'views/'
    url = {}
    front = True
    path = ''
    app_path = ''

    def init(self, environ):
        data_return = {}
        data_return['status'] = "200 OK"
        data_return['content_type'] = 'text/html; charset=utf-8'
        data_return['extra'] = self.parse_extra(
            parse_qs(environ['QUERY_STRING']))
        data_return['url'] = self.parse_url(environ['PATH_INFO'])
        config = self.get_config()
        site = environ['SERVER_NAME']
        subdirectorio = config['dir']
        https = "https://" if config['https'] else "http://"
        www = "www." if config['www'] else ""

        self.path = https + www + site + "/"
        if subdirectorio != '':
            self.path += subdirectorio + "/"
            subdirectorio = "/" + subdirectorio + "/"
        else:
            subdirectorio = "/"

        if(data_return['url'][0] == config['admin']):
            del data_return['url'][0]
            self.front = False

        if self.front:
            self.controller_dir += 'front/'+config['theme']+'/'
            self.view_dir += 'front/'+config['theme']+'/'
        else:
            self.controller_dir += 'back/'+config['theme_back']+'/'
            self.view_dir += 'back/'+config['theme_back']+'/'

        my_file = Path('../'+self.controller_dir+data_return['url'][0]+'.py')
        if my_file.is_file():
            view.add('existe', 'si')
            sys.path.insert(0, self.controller_dir)
            module = importlib.import_module(data_return['url'][0]+'.py')
        else:
            view.add('existe', 'no')
            view.add('ruta', self.controller_dir+data_return['url'][0]+'.py')

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
        if len(app.config) == 0:
            with open(self.app_dir+'config/config.json') as f:
                app.config = json.load(f)
        return app.config
