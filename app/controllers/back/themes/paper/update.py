from .base import base

#from app.models.table import table as table_model
from app.models.administrador import administrador as administrador_model
#from app.models.modulo import modulo as modulo_model
#from app.models.moduloconfiguracion import moduloconfiguracion as moduloconfiguracion_model

#from .detalle import detalle as detalle_class
#from .lista import lista as lista_class
from .head import head
from .header import header
from .aside import aside
from .footer import footer

from core.app import app
#from core.database import database
from core.functions import functions
#from core.image import image

import json
import os
from pathlib import Path


class update(base):
    url = ['update']
    metadata = {'title': 'update', 'modulo': 'update'}
    breadcrumb = []
    url_update = "http://update.mysitio.cl/"
    dir = ''
    dir_update = ''
    archivo_log = ''
    no_update = ['app\\config\\config.json', 'app/config/config.json']

    def __init__(self):
        self.dir = app.get_dir(True)
        self.dir_update = self.dir + 'update/'
        self.archivo_log = app.get_dir() + '/log.json'

    @classmethod
    def index(cls):
        ret = {'body': []}
        url_final = cls.url.copy()
        if not administrador_model.verificar_sesion():
            url_final = ['login', 'index', 'home']

        url_return = functions.url_redirect(url_final)
        if url_return != '':
            ret['error'] = 301
            ret['redirect'] = url_return
            return ret

        h = head(cls.metadata)
        ret_head = h.normal()
        if ret_head['headers'] != '':
            return ret_head
        ret['body'] += ret_head['body']

        he = header()
        ret['body'] += he.normal()['body']

        asi = aside()
        ret['body'] += asi.normal()['body']
        data = {}

        data['title'] = cls.metadata['title']
        cls.breadcrumb = [{'url': functions.generar_url(
            url_final), 'title': cls.metadata['title'], 'active':'active'}]
        data['breadcrumb'] = cls.breadcrumb

        mensaje_error = ''
        my_file = Path(cls.dir_update)
        if my_file.is_file():
            if not os.access(cls.dir_update, os.W_OK):
                mensaje_error = 'Debes dar permisos de escritura al directorio ' + cls.dir_update
        elif not os.access(dir, os.W_OK):
            mensaje_error = 'Debes dar permisos de escritura en ' + dir + \
                ' o crear el directorio update/ con permisos de escritura'

        data['mensaje_error'] = mensaje_error
        data['progreso'] = 0
        ret['body'].append(('update', data))

        f = footer()
        ret['body'] += f.normal()['body']

        return ret
    
    def vaciar_log(self):
        ret = {'body': ''}
        my_file = Path(self.archivo_log)
        if my_file.is_file():
            os.remove(self.archivo_log)
        ret['body'] = "'True'"
        return ret

    

    def  get_update(self):
        '''Obtener nuevas actualizaciones desde url_update'''
        import urllib.request
        from distutils.version import LooseVersion, StrictVersion
        ret = {'headers': [ ('Content-Type', 'application/json charset=utf-8')], 'body': ''}
        respuesta     = {'exito' : False}
        url           = self.url_update
        file = urllib.request.urlopen(url).read()
        file          = json.loads(file)
        version_mayor = {'version' : '0.0.0'}

        for f in file:
            if (version_compare(f['version'], version_mayor['version'], '>')) {
                unset(f['archivo'])
                version_mayor = f
            }
        }

        version = configuracion_model::getByVariable('version')
        if (is_bool(version) || version_compare(version_mayor['version'], version, '>')) {
            respuesta['version'] = version_mayor
            respuesta['exito']   = true
        } else {
            respuesta['mensaje'] = 'No hay nuevas actualizaciones'
        }
        echo json_encode(respuesta)
        exit()
    }
