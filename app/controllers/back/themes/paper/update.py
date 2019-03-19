from .base import base
from app.models.update import update as update_model

#from app.models.table import table as table_model
#from app.models.administrador import administrador as administrador_model
#from app.models.modulo import modulo as modulo_model
#from app.models.moduloconfiguracion import moduloconfiguracion as moduloconfiguracion_model

#from .detalle import detalle as detalle_class
#from .lista import lista as lista_class
#from .head import head
#from .header import header
#from .aside import aside
#from .footer import footer

from core.app import app
#from core.database import database
#from core.functions import functions
#from core.image import image

#import json

class update(base):
    url = ['update']
    metadata = {'title' : 'update','modulo':'update'}
    breadcrumb = []
    url_update  = "http://update.mysitio.cl/"
    dir         = ''
    dir_update  = ''
    archivo_log = ''
    no_update   = ['app\\config\\config.json','app/config/config.json']

    def __init__(self):
        self.dir         = app.get_dir(True);
        self.dir_update  = self.dir + 'update';
        self.archivo_log = app.get_dir() + '/log.json';