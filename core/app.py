# import cgitb
# cgitb.enable()
import sys
import os
from .view import view
import json
from pathlib import Path
import importlib


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
        from .cache import cache
        from .functions import functions

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

        url_cache = url.copy()
        file_cache = cache.get_cache(url_cache)
        if file_cache != '':
            response = {
                'file': file_cache,
                'is_file': True,
                'body': '', 'headers': [
                    ('Content-Type', 'text/html; charset=utf-8'),
                    ('Accept-encoding', 'gzip,deflate'),
                    ('Content-Encoding', 'gzip')]
            }
        else:
            controller = app.controller_dir + url[0]
            my_file = Path(app.root + controller + '.py')
            if my_file.is_file():
                current_module = importlib.import_module(
                    controller.replace("/", "."))
                current_module = getattr(current_module, url[0])
                current_module = current_module()
                del url[0]
                # returns {'body':[],'headers':str} or {'error':int,...'redirect':str}
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
                if not config['debug']:
                    my_file = ''
                controller = app.controller_dir + 'error'
                my_file = Path(app.root + controller + '.py')
                if my_file.is_file():
                    current_module = importlib.import_module( controller.replace("/", "."))
                    current_module = getattr(current_module, 'error')
                    current_module = current_module()
                    response_error = current_module.init(str(my_file))
                    #response_error = current_module.index(str(my_file))
                    response['body'] = response_error['body']
                else:
                    response['body'] = '<html><body>No encontrado ' + \
                        str(my_file) + '</body></html>'
        else:
            data_return['status'] = '200 OK'

        if 'is_file' in response:
            data_return['is_file'] = response['is_file']
        if 'file' in response:
            data_return['file'] = response['file']

        if isinstance(response['body'], list):
            data_return['response_body'] = view.render(response['body'])
            cache.save_cache(url_cache)
        else:
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
        for k, u in url.items():
            if len(u) == 1:
                url[k] = u[0]
        url = app.format_array(url)
        url = app.parse_values(url)
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
        try:
            for key in p.keys():
                post[key] = p[key].value
        except Exception as error:
            #raise RuntimeError('Error al obtener post: ' + repr(error) + repr(p)+ app.environ['PATH_INFO'])
            pass

        post = app.format_array(post)
        post = app.parse_values(post)
        return post

    @staticmethod
    def format_array(var_original: dict):
        var = var_original.copy()
        var_copy = var.copy()
        aux = {}
        for k, i in var_copy.items():
            # si existe simbolo de array
            if "[" in k:
                # separar key principal de key dentro de array
                final_key, rest = str(k).split('[', 1)
                if rest != '':
                    if final_key not in aux:
                        aux[final_key] = {}

                    # comprobar si existe simbolo de cerrado, sino se guarda directamente
                    if rest.find(']') == -1:
                        aux[final_key][rest] = i
                    # comprobar si existe mas de un valor en sub key, sino se recupera el primer y unico valor
                    elif rest.find('[') == -1:
                        rest = str(rest).split(']', 1)[0]
                        aux[final_key][rest] = i
                    else:
                        if rest.find(']') < rest.find('['):
                            rest1, rest2 = str(rest).split(']', 1)
                            aux[final_key][rest1+rest2] = i
                        else:
                            print(
                                'error de formato, formato aceptado: a[b][c][d]=valor')
                            break
                    aux[final_key] = app.format_array(aux[final_key])
                else:
                    aux[final_key] = i
                del var[k]
            elif k == '':
                final_key = len(var_copy)-1
                aux[final_key] = i
                del var[k]

        var = app.merge(var, aux)
        return var

    @staticmethod
    def parse_values(var: dict):
        var_copy = var.copy()
        if isinstance(var_copy, list):
            var_copy = dict.fromkeys(var_copy, 1)
        for k, i in var_copy.items():
            if isinstance(i, str):
                try:
                    aux_var = json.loads(i)
                    if isinstance(aux_var, dict) or isinstance(aux_var, list):
                        var_copy[k] = aux_var
                except:
                    pass
            elif isinstance(i, dict) or isinstance(i, list):
                var_copy[k] = app.parse_values(i)
        return var_copy

    @staticmethod
    def merge(a, b, path=None):
        "merges b into a"
        if path is None:
            path = []
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    app.merge(a[key], b[key], path + [str(key)])
                elif a[key] == b[key]:
                    pass  # same leaf value
                else:
                    raise Exception('Conflict at %s' %
                                    '.'.join(path + [str(key)]))
            else:
                a[key] = b[key]
        return a

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
