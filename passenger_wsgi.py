import sys
import os
from core import app
import linecache
from wsgiref.simple_server import make_server
from cgi import parse_qs, escape

sys.path.insert(0, os.getcwd())
#sys.path.insert(0, os.path.dirname(__file__))

def application(environ, start_response):
    try:
        main_data=app.init(environ)
        status = main_data.status
        response_headers = [
            ('Content-Type', main_data.content_type),
            ('Content-Length', str(len(main_data.response_body)))
        ]

        start_response(status, response_headers)
        return [main_data.response_body]
    except:                                   # Error output starts here
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        es = '''Error in {}, Line {} "{}": {}'''.format(filename, lineno, line.strip(), exc_obj)
        start_response('200 OK', [('Content-type', 'text/html'),])
        return [es]