from core.app import app
from pathlib import Path
import os


class static_file:
    def init(self,var=[]):
        if 0 in var:
            resource=app.get_dir(True)+var[0]
            ret = {'headers': [ ('Content-Type', 'application/json; charset=utf-8') ], 'body': ''}
            
            my_file = Path(resource)
            ret['is_file'] = True
            if my_file.is_file():
                ret['file'] = resource
            else:
                file_write = open(resource, 'w+')
                file_write.close()
                ret['file'] = resource
            return ret
        else:
            ret = {
                'error': 404
            }
            return ret
