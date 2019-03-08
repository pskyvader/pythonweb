from .base import base

from app.models.table import table as table_model
from app.models.administrador import administrador as administrador_model

#from .detalle import detalle as detalle_class
#from .lista import lista as lista_class
from .head import head
from .header import header
from .aside import aside
from .footer import footer

#from core.app import app
from core.functions import functions
#from core.image import image


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
        ret = {'body': ''}
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
