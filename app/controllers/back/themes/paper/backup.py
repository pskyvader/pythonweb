from .base import base

from core.app import app

class backup(base):
    url = ['backup']
    metadata = {'title' : 'backup','modulo':'backup'}
    breadcrumb = []
    dir_base         = ''
    dir_backup  = ''
    archivo_log = ''
    no_restore   = ['backup/']
    
    def __init__(self):
        self.dir_base         = app.get_dir(True)
        self.dir_backup  = self.dir_base + 'backup'
        self.archivo_log = app.get_dir() + '/log.json'
    