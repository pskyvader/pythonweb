# import cgitb
# cgitb.enable()
import sys
import os
from .view import view
import json
from pathlib import Path
import importlib
from importlib import util


class app:
    config = {}
    app_dir = 'app/'
    controller_dir = app_dir + 'controllers/'
    view_dir = app_dir + 'views/'
    title = ""
    prefix_site = ""
    url = {}
    front = True
    path = ''
    root = ''
    environ = {}
    get = {}

    def __init__(self, root):
        app.root = root + '/'

    def init(self, environ):
        from core.functions import functions
        app.environ = environ
        data_return = {}
        app.get = self.parse_get()
        app.post = self.parse_post()
        app.session = self.parse_session()
        url = self.parse_url(environ['PATH_INFO'])

        config = self.get_config()
        app.title = config['title']
        app.prefix_site = functions.url_amigable(app.title)

        site = environ['SERVER_NAME']
        subdirectorio = config['dir']
        https = "https://" if config['https'] else "http://"
        www = "www." if config['www'] else ""

        app.path = https + www + site + "/"
        if subdirectorio != '':
            app.path += subdirectorio + "/"
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

        app.url['base'] = app.path
        app.url['admin'] = app.path + config['admin'] + '/'

        app.url['base_dir'] = app.root+'/'
        app.url['admin_dir'] = app.root+'/' + config['admin'] + '/'

        app.url['base_sub'] = subdirectorio
        app.url['admin_sub'] = subdirectorio + config['admin'] + '/'

        if app.front:
            app.controller_dir = app.app_dir +  \
                'controllers/front/themes/' + config['theme'] + '/'
            app.view_dir = app.app_dir +  \
                'views/front/themes/' + config['theme'] + '/'
        else:
            app.path = app.url['admin']
            app.controller_dir = app.app_dir + 'controllers/' +  \
                'back/themes/' + config['theme_back'] + '/'
            app.view_dir = app.app_dir + 'views/' +  \
                'back/themes/' + config['theme_back'] + '/'

        view.set_theme(app.root + app.view_dir)

        controller = app.controller_dir + url[0]
        my_file = Path(app.root + controller + '.py')
        if my_file.is_file():
            print(controller.replace("/", ".")+'.'+url[0])
            current_module = importlib.import_module(controller.replace("/", ".")+'.'+url[0])
            del url[0]
            print(current_module)
            current_module=current_module()
            # returns {'body':str,'headers':str} or {'error':int,...'redirect':str}
            response = current_module.init(url)
        else:
            response = {'error': 404}

        if 'headers' not in response:
            response['headers'] = [
                ('Content-Type', 'text/html; charset=utf-8')
            ]

        if 'error' in response:
            if response['error'] == 301:
                if config['debug']:
                    data_return['status'] = '200 OK'
                    response['body'] = '<html><body>redirige <a href="' +  \
                        response['redirect'] + '">' +  \
                        response['redirect'] + '</a></body></html>'
                else:
                    data_return['status'] = '301 Moved Permanently'
                    response['headers'] = [('Location', response['redirect'])]
                    response['body'] = ''
            else:
                data_return['status'] = '404 Not Found'
                response['body'] = '<html><body>No encontrado ' +  \
                    str(my_file) + '</body></html>'
        else:
            data_return['status'] = '200 OK'

        if 'is_file' in response:
            data_return['is_file'] = response['is_file']
        if 'file' in response:
            data_return['file'] = response['file']

        data_return['response_body'] = response['body']
        data_return['headers'] = response['headers']
        for cookie in functions.cookies:
            data_return['headers'].append(('Set-Cookie', cookie))

        return data_return

    @staticmethod
    def parse_url(url):
        url = url.lstrip('/')
        if url != '':
            url = url.split('/')
            url = ' '.join(url).split()
            if len(url) > 0:
                if url[0] == 'manifest.js':
                    url[0] = 'manifest'
                elif url[0] == 'sw.js':
                    url[0] = 'sw'
                elif url[0] == 'favicon.ico':
                    url[0] = 'favicon'
                elif len(url) > 1:
                    if url[1] == 'manifest.js':
                        url[1] = 'manifest'
                    elif url[1] == 'sw.js':
                        url[1] = 'sw'
                    elif url[1] == 'favicon.ico':
                        url[1] = 'favicon'

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
        from cgi import FieldStorage
        post_env = app.environ.copy()
        post_env['QUERY_STRING'] = ''
        p = FieldStorage(
            fp=app.environ['wsgi.input'],
            environ=post_env,
            keep_blank_values=True
        )
        post = {}
        for key in p.keys():
            post[key] = p[key].value
        return post

    @staticmethod
    def parse_session():
        session = app.environ['beaker.session']
        return session

    @staticmethod
    def get_config():
        if len(app.config) == 0:
            with open(app.app_dir + 'config/config.json') as f:
                app.config = json.load(f)
        return app.config

    @staticmethod
    def get_dir(front=False):
        if app.front or front:
            return app.url['base_dir']
        else:
            return app.url['admin_dir']

    @staticmethod
    def get_url(front=False):
        if (app.front or front):
            return app.url['base']
        else:
            return app.url['admin']
