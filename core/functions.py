from core.app import app
from pathlib import Path
from urllib.parse import urlencode
from os.path import getmtime


class functions():
    cookies=[]
    @staticmethod
    def get_cookie(find_cookie):
        from http import cookies
        c = cookies.SimpleCookie()
        c.load(app.environ['HTTP_COOKIE'])
        if find_cookie in c:
            print(c[find_cookie].value)
            return c[find_cookie].value
        else:
            return False

    @staticmethod
    def set_cookie(cookie, value, time):
        from http import cookies
        from datetime import datetime
        c = cookies.SimpleCookie()
        # c=cookie.load(app.environ['HTTP_COOKIE'])
        directory = app.url['base_sub'] if app.front else app.url['admin_sub']
        c[cookie] = value
        c[cookie]["path"] = directory
        c[cookie]["expires"] = time
        functions.cookies.append(c[cookie].OutputString())
        return True

    @staticmethod
    def url_redirect(url):
        ruta = functions.generar_url(url)
        current = functions.current_url()
        if (ruta != current):
            return ruta
        else:
            return ""

    @staticmethod
    def generar_url(url, extra={}, front_auto=True, front=True):
        url = '/'.join(map(str, url))
        if isinstance(extra, dict) and len(extra) > 0:
            url = url+"?" + urlencode(extra, 'utf-8')
        else:
            if (len(app.get) > 0):
                if not isinstance(extra, bool) or extra == True:
                    url = url+"?" + urlencode(app.get, 'utf-8')

        url = (app.get_url() if front_auto else app.get_url(front)) + url
        return url

    @staticmethod
    def current_url():
        environ = app.environ
        url = environ['wsgi.url_scheme']+'://'
        if environ.get('HTTP_HOST'):
            url += environ['HTTP_HOST']
        else:
            url += environ['SERVER_NAME']

            if environ['wsgi.url_scheme'] == 'https':
                if environ['SERVER_PORT'] != '443':
                    url += ':' + environ['SERVER_PORT']
            else:
                if environ['SERVER_PORT'] != '80':
                    url += ':' + environ['SERVER_PORT']
        url += environ['SCRIPT_NAME']
        url += environ['PATH_INFO']
        if len(app.get) > 0:
            url += '?' + urlencode(app.get, 'utf-8')
        return url

    @staticmethod
    def fecha_archivo(archivo, only_fecha=False, final_file=''):
        c = '?time=' if "?" not in archivo else '&time='
        ac = archivo.split('?', 2)[0]
        if final_file != '':
            archivo = final_file
        
        my_file = Path(ac)

        if only_fecha:
            return int(getmtime(ac)) if my_file.is_file() else -1
        else:
            return archivo + c + str(int(getmtime(ac))) if my_file.is_file() else ""

    @staticmethod
    def ruta(texto):
        texto = texto.strip()
        if "http" in texto or texto == '#':
            ruta = texto
        elif '.' == texto:
            ruta = ''
        else:
            ruta = "http://" + texto

        return ruta
