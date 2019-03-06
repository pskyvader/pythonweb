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
    
    def __init__(cls):
        cls.dir_base         = app.get_dir(True)
        cls.dir_backup  = cls.dir_base + 'backup'
        cls.archivo_log = app.get_dir() + '/log.json'
    