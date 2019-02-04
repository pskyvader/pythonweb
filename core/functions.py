from urllib.parse import urlencode
from collections import OrderedDict

class functions():
    environ = {}
    extra = {}
    extra = {}

    @staticmethod
    def set_variable(environ,path,extra):
        functions.environ = environ
        functions.path = path
        functions.extra = extra

    @staticmethod
    def url_redirect(url):
        ruta    = functions.generar_url(url)
        current = functions.current_url()

        if (ruta != current):
            return ruta
        else:
            return ""

    @staticmethod
    def generar_url(url, extra = [], front_auto = True, front = True):
        url='/'.join(url)
        if isinstance(extra,list) and len(extra) > 0:
            url = urlencode(url,extra)
        } elseif (count($_GET) > 0) {
            if (!is_bool($extra) || $extra) {
                $url .= "?" . http_build_query($_GET);
            }
        }
        $url = str_replace("%2F", "/", $url);
        $url = (($front_auto) ? (app::get_url()) : (app::get_url($front))) . $url;

        return $url;
    

    @staticmethod
    def current_url():
        environ = functions.environ
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
        if environ['QUERY_STRING']:
            url += '?' + environ['QUERY_STRING']
        return url
