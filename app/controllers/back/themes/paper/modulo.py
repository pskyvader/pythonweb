from .base import base
from app.models.modulo import modulo as modulo_model

#from app.models.table import table as table_model
from app.models.administrador import administrador as administrador_model
from app.models.moduloconfiguracion import moduloconfiguracion as moduloconfiguracion_model
from app.models.profile import profile as profile_model

from .detalle import detalle as detalle_class
from .lista import lista as lista_class
#from .head import head
#from .header import header
#from .aside import aside
#from .footer import footer

from core.app import app
#from core.database import database
from core.functions import functions
#from core.image import image


#import json

class modulo(base):
    url = ['modulo']
    metadata = {'title': 'Modulos', 'modulo': 'modulo'}
    breadcrumb = []
    parent_class = None
    parent = None
    tipos_recortes = {
        'recortar': {'text': 'Recortar', 'value': 'recortar'},
        'rellenar': {'text': 'Rellenar', 'value': 'rellenar'},
        'centrar': {'text': 'Centrar', 'value': 'centrar'}
    }

    tipos_menu = {
        'new': {'titulo': 'Nuevo', 'field': 'new'},
        'excel': {'titulo': 'Exportar a excel', 'field': 'excel'},
        'regenerar': {'titulo': 'Regenerar imagenes', 'field': 'regenerar'}
    }

    def __init__(self):
        super().__init__(modulo_model)
        self.parent_class = moduloconfiguracion_model()
        parent_class = self.parent_class

        if not 'idmoduloconfiguracion' in app.get:
            self.url = ['home']
        else:
            self.parent = parent_class.getById(
                app.get['idmoduloconfiguracion'])
            self.breadcrumb.pop()
            self.breadcrumb.append({'url': functions.generar_url(
                ['moduloconfiguracion']), 'title': self.parent['titulo'], 'active': ''})
            self.metadata['title'] = self.parent['titulo'] + \
                ' - ' + self.metadata['title']
            self.breadcrumb.append({'url': functions.generar_url(
                self.url), 'title': (self.metadata['title']), 'active': 'active'})

    @classmethod
    def index(cls):
        '''Controlador de lista_class de elementos base, puede ser sobreescrito en el controlador de cada modulo'''
        ret = {'body': ''}
        # Clase para enviar a controlador de lista_class
        class_name = cls.class_name
        url_final = cls.url.copy()
        parent = cls.parent

        if not administrador_model.verificar_sesion():
            url_final = ['login', 'index'] + url_final
        # verificar sesion o redireccionar a login
        url_return = functions.url_redirect(url_final)
        if url_return != '':
            ret['error'] = 301
            ret['redirect'] = url_return
            return ret

        # cabeceras y campos que se muestran en la lista_class:
        # titulo,campo de la tabla a usar, tipo (ver archivo lista_class.py funcion "field")
        th = {
            'id': {'title_th': 'ID', 'field': 0, 'type': 'text'},
            'tipo': {'title_th': 'Tipo', 'field': 'tipo', 'type': 'text'},
            'orden': {'title_th': 'Orden', 'field': 'orden', 'type': 'text'},
            'titulo': {'title_th': 'Titulo', 'field': 'titulo', 'type': 'text'},
            'aside': {'title_th': 'Aparece en aside', 'field': 'aside', 'type': 'active'},
            # 'hijos' : {'title_th' : 'Contiene hijos', 'field' : 'hijos', 'type' : 'active'},
            'copy': {'title_th': 'Copiar', 'field': 0, 'type': 'action', 'action': 'copy', 'mensaje': 'Copiando Elemento'},
            'editar': {'title_th': 'Editar', 'field': 'url_detalle', 'type': 'link'},
            'delete': {'title_th': 'Eliminar', 'field': 'delete', 'type': 'delete'},
        }

        # controlador de lista_class

        lista = lista_class(cls.metadata)
        where = {'idmoduloconfiguracion': parent[0]}

        condiciones = {}
        url_detalle = url_final.copy()
        url_detalle.append('detail')
        # obtener unicamente elementos de la pagina actual
        respuesta = lista.get_row(class_name, where, condiciones, url_detalle)

        menu = {'new': (parent['tipos'] or len(
            respuesta['row']) == 0), 'excel': False, 'regenerar': False}

        # informacion para generar la vista de lista_class
        data = {
            'breadcrumb': cls.breadcrumb,
            'th': th,
            'current_url': functions.generar_url(url_final),
            'new_url': functions.generar_url(url_detalle),
        }

        data.update(respuesta)
        data.update(menu)
        ret = lista.normal(data)
        return ret

    @classmethod
    def detail(cls, var=[]):
        '''Controlador de detalle de elementos base, puede ser sobreescrito en el controlador de cada modulo'''
        ret = {'body': ''}
        # Clase para enviar a controlador de detalle
        class_name = cls.class_name
        parent = cls.parent
        url_list = cls.url.copy()
        url_save = cls.url.copy()
        url_final = cls.url.copy()
        url_save.append('guardar')
        url_final.append('detail')

        if len(var) > 0:
            id = int(var[0])
            url_final.append(id)
            cls.metadata['title'] = 'Editar ' + cls.metadata['title']
        else:
            id = 0
            cls.metadata['title'] = 'Nuevo ' + cls.metadata['title']

        cls.breadcrumb.append({'url': functions.generar_url(
            url_final), 'title': cls.metadata['title'], 'active': 'active'})

        if not administrador_model.verificar_sesion():
            url_final = ['login', 'index'] + url_final
        # verificar sesion o redireccionar a login
        url_return = functions.url_redirect(url_final)
        if url_return != '':
            ret['error'] = 301
            ret['redirect'] = url_return
            return ret

        cls.metadata['title'] = parent['titulo'] + \
            ' - ' + cls.metadata['title']
        # cabeceras y campos que se muestran en el detalle:
        # titulo,campo de la tabla a usar, tipo (ver archivo detalle.py funcion "field")

        ta = profile_model.getAll({'estado': True})
        tipos_administrador = {}
        for t in ta:
            tipos_administrador[t['tipo']] = {
                'id': t['tipo'], 'text': t['titulo']}

        columnas_menu = {
            'field': {'title_field': 'Campo', 'field': 'field', 'type': 'multiple_hidden', 'required': True},
            'titulo': {'title_field': 'Titulo', 'field': 'titulo', 'type': 'multiple_label', 'required': True, 'col': 3},
            'estado': {'title_field': 'Estado', 'field': 'estado', 'type': 'multiple_active_array', 'required': True, 'col': 9, 'array': tipos_administrador},
        }
        columnas_mostrar = {
            'field': {'title_field': 'Campo', 'field': 'field', 'type': 'multiple_hidden', 'required': True},
            'tipo': {'title_field': 'Tipo', 'field': 'tipo', 'type': 'multiple_hidden', 'required': True},
            'titulo': {'title_field': 'Titulo', 'field': 'titulo', 'type': 'multiple_label', 'required': True, 'col': 3},
            'estado': {'title_field': 'Estado', 'field': 'estado', 'type': 'multiple_active_array', 'required': True, 'col': 9, 'array': tipos_administrador},
        }
        columnas_detalle = {
            'field': {'title_field': 'Campo', 'field': 'field', 'type': 'multiple_hidden', 'required': True},
            'tipo': {'title_field': 'Tipo', 'field': 'tipo', 'type': 'multiple_hidden', 'required': True},
            'titulo': {'title_field': 'Titulo', 'field': 'titulo', 'type': 'multiple_label', 'required': True, 'col': 2},
            'texto_ayuda': {'title_field': 'Texto de ayuda', 'field': 'texto_ayuda', 'type': 'multiple_text', 'required': False, 'col': 2},
            'required': {'title_field': 'Obligatorio', 'field': 'required', 'type': 'multiple_active', 'required': True, 'col': 2},
            'estado': {'title_field': 'Estado', 'field': 'estado', 'type': 'multiple_active_array', 'required': True, 'col': 6, 'array': tipos_administrador},
        }

        columnas_recortes = {
            'tag': {'title_field': 'Etiqueta', 'field': 'tag', 'type': 'multiple_text', 'required': True, 'col': 2},
            'titulo': {'title_field': 'Titulo', 'field': 'titulo', 'type': 'multiple_text', 'required': True, 'col': 2},
            'ancho': {'title_field': 'Ancho', 'field': 'ancho', 'type': 'multiple_text', 'required': True, 'col': 1},
            'alto': {'title_field': 'Alto', 'field': 'alto', 'type': 'multiple_text', 'required': True, 'col': 1},
            'calidad': {'title_field': 'Calidad', 'field': 'calidad', 'type': 'multiple_number', 'required': True, 'col': 2, 'max': 100, 'default': 90},
            'tipo': {'title_field': 'Tipo', 'field': 'tipo', 'type': 'multiple_select', 'required': True, 'option': cls.tipos_recortes, 'col': 2},
            'button': {'field': '', 'type': 'multiple_button', 'col': 2},
        }
        columnas_estado = {
            'estado': {'title_field': 'Estado', 'field': 'estado', 'type': 'multiple_active_array', 'required': True, 'col': 9, 'array': tipos_administrador},
        }
        campos = {
            'idmoduloconfiguracion': {'title_field': 'idmoduloconfiguracion', 'field': 'idmoduloconfiguracion', 'type': 'hidden', 'required': True},
            'titulo': {'title_field': 'Titulo', 'field': 'titulo', 'type': 'text', 'required': True},
            'menu': {'title_field': 'Menu', 'field': 'menu', 'type': 'multiple', 'required': True, 'columnas': columnas_menu},
            'mostrar': {'title_field': 'Mostrar', 'field': 'mostrar', 'type': 'multiple', 'required': True, 'columnas': columnas_mostrar},
            'detalle': {'title_field': 'Detalle', 'field': 'detalle', 'type': 'multiple', 'required': True, 'columnas': columnas_detalle},
            'recortes': {'title_field': 'Imagenes', 'field': 'recortes', 'type': 'multiple', 'required': True, 'columnas': columnas_recortes},
            'tipo': {'title_field': 'Tipo', 'field': 'tipo', 'type': 'number', 'required': True},
            'orden': {'title_field': 'Orden', 'field': 'orden', 'type': 'number', 'required': True},
            'estado': {'title_field': 'Estado', 'field': 'estado', 'type': 'multiple', 'required': True, 'columnas': columnas_estado},
            'aside': {'title_field': 'Aside', 'field': 'aside', 'type': 'active', 'required': True},
            'hijos': {'title_field': 'Contiene hijos', 'field': 'hijos', 'type': 'active', 'required': True},
        }

        # controlador de detalle
        detalle = detalle_class(cls.metadata)

        row = class_name.getById(id) if id != 0 else []

        if not parent['tipos']:
            campos['tipo']['type'] = 'hidden'
            row['tipo'] = 0

        if 'menu' in row:
            for k, m in row['menu'].items():
                row['menu'][m['field']] = m

        menu = []
        for p in cls.tipos_menu.values():
            t = {}
            if 'menu' in row and p['field'] in row['menu']:
                t = row['menu'][p['field']]
            t.update(p)
            menu.append(t)

        row['menu'] = menu

        if 'mostrar' in row:
            for k, m in row['mostrar'].items():
                row['mostrar'][m['field']] = m

        mostrar = []
        if isinstance(parent['mostrar'], dict):
            for p in parent['mostrar'].values():
                t = {}
            if 'mostrar' in row and p['field'] in row['mostrar']:
                t = row['mostrar'][p['field']]
            t.update(p)
            mostrar.append(t)

        row['mostrar'] = mostrar

        if 'detalle' in row:
            for k, m in row['detalle'].items():
                row['detalle'][m['field']] = m

        det = []
        if isinstance(parent['detalle'], dict):
            for p in parent['detalle'].values():
                t = {}
            if 'detalle' in row and p['field'] in row['detalle']:
                t = row['detalle'][p['field']]
            t.update(p)
            det.append(t)

        row['detalle'] = det

        if id == 0:
            estados = {}
            for key, ta in tipos_administrador.items():
                estados[key] = "True"

            row['estado'] = [{'estado': estados}]

        row['idmoduloconfiguracion'] = parent[0]

        # informacion para generar la vista del detalle
        data = {
            'breadcrumb': cls.breadcrumb,
            'campos': campos,
            'row': row,
            'id': id if id != 0 else '',
            'current_url': functions.generar_url(url_final),
            'save_url': functions.generar_url(url_save),
            'list_url': functions.generar_url(url_list),
        }

        ret = detalle.normal(data)
        return ret
