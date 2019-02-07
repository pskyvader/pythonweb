from core.app import app
from pathlib import Path
from urllib.parse import urlencode
from os.path import getmtime


class functions():
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
    def fecha_archivo(archivo, only_fecha=False,final_file=''):
        c = '?time=' if "?" not in archivo else '&time='
        ac = archivo.split('?', 2)
        if final_file!='':
            archivo=final_file
            
        ac = ac[0]
        my_file = Path(ac)

        if only_fecha:
            return getmtime(ac) if not my_file.is_file() else False
        else:
            return archivo + c + getmtime(ac) if not my_file.is_file() else ""

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
