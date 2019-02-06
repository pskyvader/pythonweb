# import cgitb
# cgitb.enable()
import sys
import os
from core.view import view
from core.functions import functions
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
    root = ''
    environ = {}
    get = {}
    post = {}

    def __init__(self, root):
        app.root = root+'/'

    def init(self, environ):
        app.environ = environ
        data_return = {}
        app.get = self.parse_get()
        app.post = self.parse_post()
        url = self.parse_url(environ['PATH_INFO'])
        config = self.get_config()
        site = environ['SERVER_NAME']
        subdirectorio = config['dir']
        https = "https://" if config['https'] else "http://"
        www = "www." if config['www'] else ""

        app.path = https + www + site + "/"
        if subdirectorio != '':
            self.path += subdirectorio + "/"
            subdirectorio = "/" + subdirectorio + "/"
        else:
            subdirectorio = "/"

        if(url[0] == config['admin']):
            app.front = False
            del url[0]
            if len(url) == 0:
                url = ['home']
        else:
            app.front = True

        if app.front:
            app.controller_dir = app.app_dir + \
                'controllers/front/themes/'+config['theme']+'/'
            app.view_dir = app.app_dir + \
                'views/front/themes/'+config['theme']+'/'
        else:
            app.controller_dir = app.app_dir+'controllers/' + \
                'back/themes/'+config['theme_back']+'/'
            app.view_dir = app.app_dir+'views/' + \
                'back/themes/'+config['theme_back']+'/'

        app.url['base'] = app.path
        app.url['admin'] = app.path+config['admin']+'/'

        view.set_theme(app.root+app.view_dir)

        controller = app.controller_dir+url[0]
        my_file = Path(app.root+controller+'.py')
        if my_file.is_file():
            current_module = importlib.import_module(
                controller.replace("/", "."))
            del url[0]
            # returns {'body':str,'headers':str} or {'error':int,...'redirect':str}
            response = current_module.init(url)
        else:
            response = {'error': 404}


        if 'headers' not in data_return:
            response['headers'] = [
                ('Content-Type', 'text/html; charset=utf-8')
            ]
        if 'error' in response:
            if response['error'] == 301:
                if config['debug']:
                    data_return['status'] = '200 OK'
                    response['body'] = '<html><body>redirige <a href="' + \
                        response['redirect']+'">' + \
                        response['redirect']+'</a></body></html>'
                else:
                    data_return['status'] = '301 Moved Permanently'
                    response['headers'] = [('Location', response['redirect'])]
                    response['body'] = ''
            else:
                data_return['status'] = '404 Not Found'
                response['body'] = '<html><body>No encontrado ' + \
                    str(my_file)+'</body></html>'
        else:
            data_return['status'] = '200 OK'

        data_return['response_body'] = response['body']
        data_return['headers'] = response['headers']

        return data_return

    @staticmethod
    def parse_url(url):
        url = url.lstrip('/')
        if url != '':
            url = url.split('/')
            url = ' '.join(url).split()
            if url[0] == 'manifest.js':
                url[0] = 'manifest'
            else:
                if url[0] == 'sw.js':
                    url[0] = 'sw'
        else:
            url = ['home']
        return url

    @staticmethod
    def parse_get():
        from cgi import parse_qs
        url = dict(parse_qs(app.environ['QUERY_STRING']))
        if 'url' in url:
            del url['url']
        return url

    @staticmethod
    def parse_post():
        url = app.environ['wsgi.input']
        return url

    @staticmethod
    def get_config():
        if len(app.config) == 0:
            with open(app.app_dir+'config/config.json') as f:
                app.config = json.load(f)
        return app.config

    @staticmethod
    def get_url(front=False):
        if (app.front or front):
            return app.url['base']
        else:
            return app.url['admin']
