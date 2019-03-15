from core.app import app
from pathlib import Path
import os
import mimetypes


class static_file:
    def init(self,var=[]):
        if len(var)>0:
            resource_url=app.get_dir(True)+var[0]
            mime = mimetypes.guess_type(resource_url, False)[0]
            if mime == None:
                mime = 'text/plain'
            ret = {'headers': [ 'Content-Type', mime+'; charset=utf-8' ], 'body': ''}
            
            my_file = Path(resource_url)
            ret['is_file'] = True
            if my_file.is_file():
                ret['file'] = resource_url
            else:
                file_write = open(resource_url, 'w+')
                file_write.close()
                ret['file'] = resource_url
            return ret
        else:
            ret = {
                'error': 404
            }
            return ret
