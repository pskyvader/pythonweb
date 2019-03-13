from core.view import view
from core.app import app

import os
from pathlib import Path
from core.functions import functions
import mimetypes
import datetime
import socket


class logging:
    def init(self,var=[]):
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
