import sys
import os
from core import app
import linecache
from wsgiref.simple_server import make_server

sys.path.insert(0, os.path.dirname(__file__))


def application(environ, start_response):
        app_web=app.app(os.path.dirname(__file__))
        main_data = app_web.init(environ)
        start_response(main_data['status'], main_data['headers'])
    try:
        ret = main_data['response_body']
    except:                                   # Error output starts here
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        es = '''Error in {}, Line {} "{}": {}'''.format(
            filename, lineno, line.strip(), exc_obj)
        start_response('500 Internal Server Error', [
                       ('Content-type', 'text/html; charset=utf-8'), ])
        ret = es

    return [bytes(ret, 'utf-8')]
