from .base import base

from app.models.table import table as table_model
from app.models.administrador import administrador as administrador_model
from app.models.modulo import modulo as modulo_model
from app.models.moduloconfiguracion import moduloconfiguracion as moduloconfiguracion_model

#from .detalle import detalle as detalle_class
#from .lista import lista as lista_class
from .head import head
from .header import header
from .aside import aside
from .footer import footer

from core.app import app
from core.database import database
from core.cache import cache
from core.functions import functions
#from core.image import image

import json


class configuracionadministrador(base):
    url = ['configuracionadministrador']
    metadata = {'title': 'Configuracion de administrador',
                'modulo': 'configuracionadministrador'}
    breadcrumb = []

    def __init__(self):
        super().__init__(None)

    @classmethod
    def index(cls):
        '''Controlador de lista_class de elementos base, puede ser sobreescrito en el controlador de cada modulo'''
        ret = {'body': []}
        # Clase para enviar a controlador de lista_class
        url_final = cls.url.copy()
        if not administrador_model.verificar_sesion():
            url_final = ['login', 'index'] + url_final
        # verificar sesion o redireccionar a login
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

        vaciar = table_model.getAll({'truncate': True}, {}, 'tablename')
        data = {}
        data['vaciar'] = vaciar
        data['breadcrumb'] = cls.breadcrumb
        data['title'] = cls.metadata['title']
        data['save_url'] = functions.generar_url(cls.url + ['vaciar'])
        data['list_url'] = functions.generar_url(cls.url)

        ret['body'].append(('configuracion_administrador', data))

        f = footer()
        ret['body'] += f.normal()['body']

        return ret

    def vaciar(self):
        ret = {'body': []}
        post = app.post
        if 'campos' in post:
            campos = post['campos']
            respuesta = table_model.truncate(campos)
            cache.delete_cache()
        else:
            respuesta = {'exito': False,
                         'mensaje': 'Debe seleccionar una tabla para vaciar'}
        ret['body'] = json.dumps(respuesta)
        return ret

    def json(self,responder = True):
        respuesta = {'exito' : True, 'mensaje' : 'JSON generado correctamente'}
        
        base_dir       = app.get_dir(True) + '/config/'
        row       = table_model.getAll()
        campos    = []
        for tabla in row.values():
            a = {
                'tablename' : tabla['tablename'],
                'idname'    : tabla['idname'],
                'fields'    : tabla['fields'],
                'truncate'  : tabla['truncate'],
            }
            campos.append(a)

        file_write = open(base_dir + 'bdd.json', 'w')
        file_write.write(json.dumps(campos))
        file_write.close()

        row         = moduloconfiguracion_model.getAll()
        campos      = []
        fields      = table_model.getByname('moduloconfiguracion')
        fields_hijo = table_model.getByname('modulo')
        for tabla in row.values():
            a        = database.create_data(fields, tabla)
            row_hijo = modulo_model.getAll(array('idmoduloconfiguracion' : tabla[0]))
            h        = array()

            foreach (row_hijo as key : hijos) {
                h[] = database.create_data(fields_hijo, hijos)
            }
            a['hijo'] = h
            campos[]  = a
        }
        file_put_contents(base_dir . 'moduloconfiguracion.json', functions.encode_json(campos, True))

        row    = configuracion_model.getAll()
        campos = array()
        fields = table_model.getByname('configuracion')
        foreach (row as key : tabla) {
            a        = database.create_data(fields, tabla)
            campos[] = a
        }
        file_put_contents(base_dir . 'configuracion.json', functions.encode_json(campos, True))
        if (responder) {
            echo json_encode(respuesta)
        }
    }