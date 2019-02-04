
def current_url(environ):
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
    url += environ.get('SCRIPT_NAME', '')
    url += environ.get('PATH_INFO', '')
    if environ.get('QUERY_STRING'):
        url += '?' + environ['QUERY_STRING']
    return url
