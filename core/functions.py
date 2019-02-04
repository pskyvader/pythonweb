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
        from core.app import app
        from urllib.parse import urlencode
        from urllib.parse import quote
        url = '/'.join(url)
        if isinstance(extra, dict) and len(extra) > 0:
            url = url+"?" + quote(extra)
        else:
            if (len(app.extra) > 0):
                if not isinstance(extra, bool) or extra == True:
                    url = url+"?" + urlencode(app.extra)

        url = (app.get_url() if front_auto else app.get_url(front)) + url
        return url

    @staticmethod
    def current_url():
        from core.app import app
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
        if environ['QUERY_STRING']:
            url += '?' + environ['QUERY_STRING']
        return url
