from core.app import app
class functions(app):
    def __init__(self, root):
        super().__init__(root)

    @staticmethod
    def current_url():
        url = app.environ['wsgi.url_scheme']+'://'
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
