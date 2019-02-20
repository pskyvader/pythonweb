import sys
import os
from core.app import app
import pprint
from beaker.middleware import SessionMiddleware

sys.path.insert(0, os.path.dirname(__file__))

def application2(environ, start_response):
    app_web = app(os.path.dirname(__file__))
    main_data = app_web.init(environ)
    start_response(main_data['status'], main_data['headers'])
    ret = main_data['response_body']
    if isinstance(ret, str):
        return [bytes(ret, 'utf-8')]
    else:
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


application = LoggingMiddleware(application2)
