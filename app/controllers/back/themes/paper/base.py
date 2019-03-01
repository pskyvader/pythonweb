from core.app import app
from core.functions import functions
from app.models.moduloconfiguracion import moduloconfiguracion as moduloconfiguracion_model
from app.models.modulo import modulo as modulo_model
import importlib


class base:
    url = []
    metadata = {}
    class_name = None
    breadcrumb = []
    contiene_tipos = False
    contiene_hijos = False

    def __init__(self, class_name=None):
        moduloconfiguracion = moduloconfiguracion_model.getByModulo(self.metadata['modulo'])
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
    def init(cls, var):
        from inspect import signature

        if len(var)==0:
            var=['index']

        if hasattr(cls, var[0]) and callable(getattr(cls, var[0])):
            fun = var[0]
            del var[0]
            method = getattr(cls, fun)
            sig = signature(method)
            params = sig.parameters 
            if len(params)>=1:
                ret = method(var)
            else:
                ret=method()
        else:
            ret = {
                'error': 404
            }
        return ret
