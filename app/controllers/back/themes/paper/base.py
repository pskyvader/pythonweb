from core.app import app
from app.models.moduloconfiguracion import moduloconfiguracion as moduloconfiguracion_model
from app.models.modulo import modulo as modulo_model
import importlib



class base:
    url            = []
    metadata       = {}
    class_name          = None
    breadcrumb     = []
    contiene_tipos = False
    contiene_hijos = False

    @classmethod
    def __init__(cls, class_name):
        moduloconfiguracion = moduloconfiguracion_model.getByModulo(cls.metadata['modulo'])
        if 0 in moduloconfiguracion:
            cls.contiene_tipos =moduloconfiguracion['tipos'] if 'tipos' in moduloconfiguracion else False
            cls.sub =moduloconfiguracion['sub'] if 'sub' in moduloconfiguracion else ''
            cls.padre =moduloconfiguracion['padre'] if 'padre' in moduloconfiguracion else ''
            
            if cls.contiene_tipos and 'tipo' in app.get:
                tipo = app.get['tipo']
            else:
                tipo = 0


            modulo                  = modulo_model.getAll({'idmoduloconfiguracion' : moduloconfiguracion[0], 'tipo' : tipo})
            cls.contiene_hijos    = (isset(modulo[0]['hijos'])) ? modulo[0]['hijos'] : false
            cls.metadata['title'] = modulo[0]['titulo']
            
            if cls.padre != '':
                parent             = 'app.models.' + cls.padre
                cls.class_parent = importlib.import_module(parent)()

                if cls.class_parent.idname in app.get:
                    p=cls.class_parent.getById(app.get[cls.class_parent.idname])
                    if len(p)>0:
                        if 'titulo' in p and p['titulo']!='':
                            cls.metadata['title']+=' - '+p['titulo']
                        elif 'nombre' in p and p['nombre']!='':
                            cls.metadata['title']+=' - '+p['nombre']
                        

        cls.class_name      = class_name
        cls.breadcrumb = [
            {'url' : functions.generar_url(["home"]), 'title' : 'Home', 'active' : ''},
            {'url' : functions.generar_url(cls.url), 'title' : (cls.metadata['title']), 'active' : 'active'},
        ]
        
    @classmethod
    def init(cls,var):
        if len(var) > 0:
            if hasattr(cls, var[0]) and callable(getattr(cls, var[0])):
                fun = var[0]
                del var[0]
                method=getattr(cls, fun)
                ret = method(var)
            else:
                ret = {
                    'error': 404,
                }
        else:
            ret = cls.index(cls)
        return ret

