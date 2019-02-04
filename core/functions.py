def current_url(environ):
    url = environ['HTTP_HOST']
    uri = environ['REQUEST_URI']
    return url + uri