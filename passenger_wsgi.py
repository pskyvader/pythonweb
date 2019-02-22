import sys
import os
from core.app import app
import pprint
from beaker.middleware import SessionMiddleware

sys.path.insert(0, os.path.dirname(__file__))

def application2(environ, start_response):
    app_web = app(os.path.dirname(__file__))
    main_data = app_web.init(environ)


    ret = main_data['response_body']

    if isinstance(ret, str) and len(ret)>0:
        ret=bytes(ret, 'utf-8')
        from gzip import compress
        ret = compress(ret)
        main_data['headers'].append(('Accept-encoding', 'gzip,deflate'))
        main_data['headers'].append(('Content-Encoding', 'gzip'))
        
    start_response(main_data['status'], main_data['headers'])

    if 'is_file' in main_data:
        print('is file',main_data['file'])
        f = open(main_data['file'], 'rb')
        return environ['wsgi.file_wrapper'](f, 32768)

    return [ret]


class LoggingMiddleware:
    
    def __init__(self, application):
        self.__application = application

    def __call__(self, environ, start_response):
        errors = environ['wsgi.errors']

        def _start_response(status, headers, *args):
            if status!="200 OK":
                pprint.pprint(('RESPONSE', status, headers), stream=errors)
            return start_response(status, headers, *args)

        return self.__application(environ, _start_response)


#application = LoggingMiddleware(application2)

session_opts = {
    'session.cookie_expires': True,
    'session.httponly': True,
    #'session.secure': True
}

app2 = LoggingMiddleware(application2)
application = SessionMiddleware(app2, session_opts)