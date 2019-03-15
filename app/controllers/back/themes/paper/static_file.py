from core.app import app
from pathlib import Path
import os


class static_file:
    def init(self,var=[]):
        print(var)
        resource=app.get_dir(True)+'log.json'
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
