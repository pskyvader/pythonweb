from .app import app
from pathlib import Path
from urllib.parse import urlencode
from os.path import getmtime


class functions():
    cookies = []
    @staticmethod
    def get_cookie(find_cookie=''):
        from http import cookies
        c = cookies.SimpleCookie()
        if 'HTTP_COOKIE' in app.environ:
            c.load(app.environ['HTTP_COOKIE'])
            if find_cookie != '':
                if find_cookie in c:
                    return c[find_cookie].value
                else:
                    return False
            else:
                coo = {}
                for key, cookie in c.items():
                    coo[key] = cookie.value
                return coo
        else:
            if find_cookie != '':
                return False
            else:
                return {}

    @staticmethod
    def set_cookie(cookie, value, time):
        from http import cookies
        c = cookies.SimpleCookie()
        # c=cookie.load(app.environ['HTTP_COOKIE'])
        directory = app.url['base_sub'] if app.front else app.url['admin_sub']
        c[cookie] = value
        c[cookie]["path"] = directory
        c[cookie]["expires"] = time
        c[cookie]["httponly"] = True
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
    def get_idseccion(url: str):
        url = url.split('-', 2)
        return int(url[0])

    @staticmethod
    def url_seccion(url_base: list, seccion=dict, return_url=False, extra_variables=False):
        url = url_base
        extra = ""
        if 0 in seccion:
            extra += seccion[0]
            if 'url' in seccion:
                extra += "-" + seccion['url']
            elif 'titulo' in seccion:
                extra += "-" + functions.url_amigable(seccion['titulo'])

        url.append(extra)
        if return_url:
            return url
        else:
            return functions.generar_url(url, extra_variables)

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
    def generar_pass(length=8):
        import string
        import secrets
        password = ''.join(secrets.choice(
            string.ascii_uppercase + string.digits) for _ in range(length))
        return password

    @staticmethod
    def url_amigable(url=""):
        url = functions.replaceMultiple(
            url, ['á', 'à', 'â', 'ã', 'ª', 'ä'], 'a')
        url = functions.replaceMultiple(url, ['Á', 'À', 'Â', 'Ã', 'Ä'], "A")
        url = functions.replaceMultiple(url, ['Í', 'Ì', 'Î', 'Ï'], "I")
        url = functions.replaceMultiple(url, ['í', 'ì', 'î', 'ï'], "i")
        url = functions.replaceMultiple(url, ['é', 'è', 'ê', 'ë'], "e")
        url = functions.replaceMultiple(url, ['É', 'È', 'Ê', 'Ë'], "E")
        url = functions.replaceMultiple(url, ['ó', 'ò', 'ô', 'õ', 'ö'], "o")
        url = functions.replaceMultiple(url, ['Ó', 'Ò', 'Ô', 'Õ', 'Ö'], "O")
        url = functions.replaceMultiple(url, ['ú', 'ù', 'û', 'ü'], "u")
        url = functions.replaceMultiple(url, ['Ú', 'Ù', 'Û', 'Ü'], "U")
        url = functions.replaceMultiple(
            url, ['[', '^', '´', '`', '¨', '~', ']', ' ', '/', '°', 'º'], "-")
        url = url.replace("ç", "c")
        url = url.replace("Ç", "C")
        url = url.replace("ñ", "n")
        url = url.replace("Ñ", "N")
        url = url.replace("Ý", "Y")
        url = url.replace("ý", "y")
        url = url.lower()
        return url

    @staticmethod
    def replaceMultiple(mainString, toBeReplaces, newString):
        # Iterate over the strings to be replaced
        for elem in toBeReplaces:
            # Check if string is in the main string
            if elem in mainString:
                # Replace the string
                mainString = mainString.replace(elem, newString)
        return mainString

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

    @staticmethod
    def crear_arbol(data: dict, idpadre=0):
        tree = {'children': {}, 'root': {}}
        for node in data:
            id = node[0]
            # Puede que exista el children creado si los hijos entran antes que el padre
            node['children'] = tree['children'][id]['children'] if id in tree['children'] else {}
            tree['children'][id] = node
            if node['idpadre'][0] == idpadre:
                tree['root'][id] = tree['children'][id]
            else:
                tree['children'][node['idpadre'][0] ]['children'][id] = tree['children'][id]

        return tree['root']
