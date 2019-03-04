from core.app import app
from core.functions import functions
from core.image import image
from core.file import file
from app.models.moduloconfiguracion import moduloconfiguracion as moduloconfiguracion_model
from app.models.modulo import modulo as modulo_model
from app.models.administrador import administrador as administrador_model
from app.models.table import table

from .lista import lista
from .detalle import detalle

import importlib
import json


class base:
    url = []
    metadata = {'title': '', 'modulo': ''}
    class_name = None
    class_parent = None
    sub = None
    breadcrumb = []
    contiene_tipos = False
    contiene_hijos = False

    @classmethod
    def init(cls, var):
        from inspect import signature

        if len(var) == 0:
            var = ['index']

        if hasattr(cls, var[0]) and callable(getattr(cls, var[0])):
            fun = var[0]
            del var[0]
            method = getattr(cls, fun)
            sig = signature(method)
            params = sig.parameters
            if len(params) >= 1:
                ret = method(var)
            else:
                ret = method()
        else:
            ret = {
                'error': 404
            }
        return ret

    def __init__(self, class_name=None):
        moduloconfiguracion = moduloconfiguracion_model.getByModulo(
            self.metadata['modulo'])
        if 0 in moduloconfiguracion:
            self.contiene_tipos = moduloconfiguracion['tipos'] if 'tipos' in moduloconfiguracion else False
            self.sub = moduloconfiguracion['sub'] if 'sub' in moduloconfiguracion else ''
            self.padre = moduloconfiguracion['padre'] if 'padre' in moduloconfiguracion else ''

            if self.contiene_tipos and 'tipo' in app.get:
                tipo = app.get['tipo']
            else:
                tipo = 0

            modulo = modulo_model.getAll(
                {'idmoduloconfiguracion': moduloconfiguracion[0], 'tipo': tipo})
            self.contiene_hijos = modulo[0]['hijos'] if 'hijos' in modulo[0] else False
            self.metadata['title'] = modulo[0]['titulo']

            if self.padre != '':
                parent = 'app.models.' + self.padre
                self.class_parent = importlib.import_module(parent)()

                if self.class_parent.idname in app.get:
                    p = self.class_parent.getById(
                        app.get[self.class_parent.idname])
                    if len(p) > 0:
                        if 'titulo' in p and p['titulo'] != '':
                            self.metadata['title'] += ' - '+p['titulo']
                        elif 'nombre' in p and p['nombre'] != '':
                            self.metadata['title'] += ' - '+p['nombre']

        self.class_name = class_name
        self.breadcrumb = [
            {'url': functions.generar_url(
                ["home"]), 'title': 'Home', 'active': ''},
            {'url': functions.generar_url(self.url), 'title': (
                self.metadata['title']), 'active': 'active'},
        ]

    @classmethod
    def index(cls):
        '''Controlador de lista de elementos base, puede ser sobreescrito en el controlador de cada modulo'''
        ret = {'body': ''}
        # Clase para enviar a controlador de lista
        class_name = cls.class_name
        get = app.get
        if cls.contiene_tipos and not 'tipo' in get:
            cls.url = ['home']
        if cls.contiene_hijos and not 'idpadre' in get:
            cls.url = ['home']

        if not administrador_model.verificar_sesion():
            cls.url = ['login', 'index'] + cls.url
        # verificar sesion o redireccionar a login
        url_return = functions.url_redirect(cls.url)
        if url_return != '':
            ret['error'] = 301
            ret['redirect'] = url_return
            return ret

        # cabeceras y campos que se muestran en la lista:
        # titulo,campo de la tabla a usar, tipo (ver archivo lista.py funcion "field")
        # controlador de lista
        list = lista(cls.metadata)
        configuracion = list.configuracion(cls.metadata['modulo'])
        if 'error' in configuracion:
            ret['error']=configuracion['error']
            ret['redirect']=configuracion['redirect']
            return ret

        where = {}
        if cls.contiene_tipos:
            where['tipo'] = get['tipo']
        if cls.contiene_hijos:
            where['idpadre'] = get['idpadre']
        if cls.class_parent != None:
            class_parent = cls.class_parent

            if class_parent.idname in get:
                where[class_parent.idname] = get[class_parent.idname]

        condiciones = {}
        url_detalle = cls.url
        url_detalle.append('detail')
        # obtener unicamente elementos de la pagina actual
        respuesta = list.get_row(class_name, where, condiciones, url_detalle)

        if 'copy' in configuracion['th']:
            configuracion['th']['copy']['action'] = configuracion['th']['copy']['field']
            configuracion['th']['copy']['field'] = 0
            configuracion['th']['copy']['mensaje'] = 'Copiando'

        if cls.contiene_hijos:
            if cls.contiene_tipos:
                for v in respuesta['row']:
                    v['url_children'] = functions.generar_url(
                        cls.url, {'idpadre': v[0], 'tipo': get['tipo']})

            else:
                for v in respuesta['row']:
                    v['url_children'] = functions.generar_url(
                        cls.url, {'idpadre': v[0]})

        else:
            del configuracion['th']['url_children']

        if cls.sub != '':
            if cls.contiene_tipos:
                for v in respuesta['row']:
                    v['url_sub'] = functions.generar_url(
                        [cls.sub], {class_name.idname: v[0], 'tipo': get['tipo']})

            else:
                for v in respuesta['row']:
                    v['url_sub'] = functions.generar_url(
                        [cls.sub], {class_name.idname: v[0]})

        else:
            del configuracion['th']['url_sub']

        # informacion para generar la vista de lista
        data = {
            'breadcrumb': cls.breadcrumb,
            'th': configuracion['th'],
            'current_url': functions.generar_url(cls.url),
            'new_url': functions.generar_url(url_detalle),
        }

        data.update(respuesta)
        data.update(configuracion['menu'])
        ret = list.normal(data)

    @classmethod
    def detail(cls, var={}):
        '''Controlador de detalle de elementos base, puede ser sobreescrito en el controlador de cada modulo'''
        ret = {'body': ''}
        # Clase para enviar a controlador de detalle
        class_name = cls.class_name
        get = app.get
        url_save = url_list = cls.url
        url_save.append('guardar')
        cls.url.append('detail')
        if 0 in var:
            id = int(var[0])
            cls.url.append(id)
            cls.metadata['title'] = 'Editar ' + cls.metadata['title']
        else:
            id = 0
            cls.metadata['title'] = 'Nuevo ' + cls.metadata['title']

        cls.breadcrumb.append({'url': functions.generar_url(
            cls.url), 'title': cls.metadata['title'], 'active': 'active'})
        if cls.contiene_tipos and 'tipo' not in get:
            cls.url = ['home']

        if not administrador_model.verificar_sesion():
            cls.url = {'login', 'index'} + cls.url
        # verificar sesion o redireccionar a login
        url_return = functions.url_redirect(cls.url)
        if url_return != '':
            ret['error'] = 301
            ret['redirect'] = url_return
            return ret

        # cabeceras y campos que se muestran en el detalle:
        # titulo,campo de la tabla a usar, tipo (ver archivo detalle.py funcion "field")

        # controlador de detalle
        detail = detalle(cls.metadata)
        configuracion = detail.configuracion(cls.metadata['modulo'])
        
        if 'error' in configuracion:
            ret['error']=configuracion['error']
            ret['redirect']=configuracion['redirect']
            return ret

        row = class_name.getById(id) if id != 0 else []
        if cls.contiene_tipos:
            configuracion['campos']['tipo'] = {
                'title_field': 'tipo', 'field': 'tipo', 'type': 'hidden', 'required': True}
            row['tipo'] = get['tipo']

        if cls.contiene_hijos and 'idpadre' in configuracion['campos']:
            categorias = class_name.getAll()
            for c in categorias:
                if c[0] == id:
                    del c
                    break

            raiz = {0: 0, 'titulo': 'Raíz', 'idpadre': [-1]}
            categorias = raiz+categorias
            configuracion['campos']['idpadre']['parent'] = functions.crear_arbol( categorias, -1)
        elif cls.contiene_hijos or 'idpadre' in configuracion['campos']:
            configuracion['campos']['idpadre'] = {
                'title_field': 'idpadre', 'field': 'idpadre', 'type': 'hidden', 'required': True}
            if id == 0:
                if 'idpadre' in get:
                    row['idpadre'] = json.dumps([get['idpadre']])
                else:
                    row['idpadre'] = json.dumps([0])
        else:
            del configuracion['campos']['idpadre']

        if cls.class_parent != None:
            class_parent = cls.class_parent
            idparent = class_parent.idname

            is_array = True
            fields = table.getByname(class_name.table)
            if idparent in fields and fields[idparent]['tipo'] != 'longtext':
                is_array = False

            if idparent in configuracion['campos']:
                categorias = class_parent.getAll()
                if is_array:
                    configuracion['campos'][idparent]['parent'] = functions.crear_arbol(
                        categorias)
                else:
                    configuracion['campos'][idparent]['parent'] = categorias

            else:
                configuracion['campos'][idparent] = {
                    'title_field': idparent, 'field': idparent, 'type': 'hidden', 'required': True}
                if id == 0:
                    if idparent in get:
                        if is_array:
                            row[idparent] = json.dumps([get[idparent]])
                        else:
                            row[idparent] = int(get[idparent])
                    else:
                        if is_array:
                            row[idparent] = json.dumps([0])
                        else:
                            row[idparent] = 0
                else:
                    if is_array:
                        row[idparent] = json.dumps(row[idparent])
                    else:
                        row[idparent] = row[idparent]

        # informacion para generar la vista del detalle
        data = {
            'breadcrumb': cls.breadcrumb,
            'campos': configuracion['campos'],
            'row': row,
            'id': id if id != 0 else '',
            'current_url': functions.generar_url(cls.url),
            'save_url': functions.generar_url(url_save),
            'list_url': functions.generar_url(url_list),
        }

        detail.normal(data, class_name)

    @classmethod
    def orden(cls):
        respuesta = {'body': ''}
        respuesta['body'] = json.dumps(lista.orden(cls.class_name))
        return respuesta

    @classmethod
    def estado(cls):
        respuesta = {'body': ''}
        respuesta['body'] = json.dumps(lista.estado(cls.class_name))
        return respuesta

    def eliminar(cls):
        respuesta = {'body': ''}
        respuesta['body'] = json.dumps(lista.eliminar(cls.class_name))
        return respuesta

    def copy(cls):
        respuesta = {'body': ''}
        respuesta['body'] = json.dumps(lista.copy(cls.class_name))
        return respuesta

    def excel(cls):
        get=app.get
        respuesta = {'body': ''}
        respuesta['body'] = {'exito': False, 'mensaje' : 'Debes recargar la pagina'}
        if cls.contiene_tipos and 'tipo' not in get:
            respuesta['body']=json.dumps(respuesta['body'])
            return respuesta
        
        if cls.contiene_hijos and 'idpadre' not in get:
            respuesta['body']=json.dumps(respuesta['body'])
            return respuesta
        
        where = {}
        if cls.contiene_tipos:
            where['tipo'] = get['tipo']
        
        if cls.contiene_hijos:
            where['idpadre'] = get['idpadre']
        
        if cls.class_parent!=None:
            class_parent = cls.class_parent
            if class_parent.idname in get:
                where[class_parent.idname] = get[class_parent.idname]
            
        
        select = ""
        respuesta['body'] = json.dumps(lista.excel(cls.class_name, where, select, cls.metadata['title']))
        return respuesta

    def get_all(cls):
        get=app.get
        respuesta = {'body': ''}
        respuesta['body'] = {'exito': False, 'mensaje' : 'Debes recargar la pagina'}
        if cls.contiene_tipos and 'tipo' not in get:
            respuesta['body']=json.dumps(respuesta['body'])
            return
        
        if cls.contiene_hijos and 'idpadre' not in get:
            respuesta['body']=json.dumps(respuesta['body'])
            return
        
        where = {}
        if cls.contiene_tipos:
            where['tipo'] = get['tipo']
        
        if cls.contiene_hijos:
            where['idpadre'] = get['idpadre']
        
        if cls.class_parent!= None:
            class_parent = cls.class_parent
            if class_parent.idname in get:
                where[class_parent.idname] = get[class_parent.idname]
            
        
        condiciones = {}
        select = ""
        class_name = cls.class_name
        row = class_name.getAll(where, condiciones, select)
        
        respuesta['body']=json.dumps(row)
        return respuesta

    def regenerar(cls):
        respuesta = {'body': ''}
        respuesta['body'] = json.dumps(image.regenerar(app.post))
        return respuesta

    def guardar(cls):
        respuesta = {'body': ''}
        respuesta['body'] = json.dumps(detalle.guardar(cls.class_name))
        return respuesta

    def upload(cls):
        respuesta = {'body': ''}
        respuesta['body'] = json.dumps(image.upload_tmp(cls.metadata['modulo']))
        return respuesta

    def upload_file(cls):
        respuesta = {'body': ''}
        respuesta['body'] = json.dumps(file.upload_tmp())
        return respuesta
