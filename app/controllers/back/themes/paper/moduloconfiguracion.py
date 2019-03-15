from .base import base
from app.models.moduloconfiguracion import moduloconfiguracion as moduloconfiguracion_model

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

#from core.app import app
#from core.database import database
from core.functions import functions
#from core.image import image


#import json

class moduloconfiguracion(base):
    url = ['moduloconfiguracion']
    metadata = {'title' : 'Configuracion de modulos','modulo':'moduloconfiguracion'}
    breadcrumb = []
    tipos_mostrar = {
        'action' : {'text' : 'Accion', 'value' : 'action'},
        'active' : {'text' : 'Active', 'value' : 'active'},
        'color' : {'text' : 'Color', 'value' : 'color'},
        'delete' : {'text' : 'Eliminar', 'value' : 'delete'},
        'image' : {'text' : 'Imagen', 'value' : 'image'},
        'link' : {'text' : 'Link', 'value' : 'link'},
        'text' : {'text' : 'Texto', 'value' : 'text'},
    }
    tipos_detalle = {
        'active' : {'text' : 'Active', 'value' : 'active'},
        'file' : {'text' : 'Archivo', 'value' : 'file'},
        'multiple_file' : {'text' : 'Archivo multiple', 'value' : 'multiple_file'},
        'recursive_checkbox' : {'text' : 'Arbol de botones checkbox', 'value' : 'recursive_checkbox'},
        'recursive_radio' : {'text' : 'Arbol de botones radio', 'value' : 'recursive_radio'},
        'color' : {'text' : 'Color', 'value' : 'color'},
        'password' : {'text' : 'Contraseña', 'value' : 'password'},
        'editor' : {'text' : 'Editor', 'value' : 'editor'},
        'email' : {'text' : 'Email', 'value' : 'email'},
        'date' : {'text' : 'Fecha', 'value' : 'date'},
        'grupo_pedido' : {'text' : 'Grupos de pedido', 'value' : 'grupo_pedido'},
        'image' : {'text' : 'Imagen', 'value' : 'image'},
        'multiple_image' : {'text' : 'Imagen multiple', 'value' : 'multiple_image'},
        'map' : {'text' : 'Mapa', 'value' : 'map'},
        'multiple' : {'text' : 'Multiple', 'value' : 'multiple'},
        'number' : {'text' : 'Numero', 'value' : 'number'},
        'daterange' : {'text' : 'Rango de fechas', 'value' : 'daterange'},
        'select' : {'text' : 'Select', 'value' : 'select'},
        'text' : {'text' : 'Texto', 'value' : 'text'},
        'textarea' : {'text' : 'Texto largo', 'value' : 'textarea'},
        'token' : {'text' : 'Token', 'value' : 'token'},
        'url' : {'text' : 'URL', 'value' : 'url'},
    }


    def __init__(self):
        super().__init__(moduloconfiguracion_model)

    @classmethod
    def index(cls):
        '''Controlador de lista_class de elementos base, puede ser sobreescrito en el controlador de cada modulo'''
        ret = {'body': ''}
        # Clase para enviar a controlador de lista_class
        class_name = cls.class_name
        url_final=cls.url.copy()
        

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
            #'id' : {'title_th' : 'ID', 'field' : 0, 'type' : 'text'},
            'orden' : {'title_th' : 'Orden', 'field' : 'orden', 'type' : 'text'},
            'module' : {'title_th' : 'Modulo', 'field' : 'module', 'type' : 'text'},
            'titulo' : {'title_th' : 'Titulo', 'field' : 'titulo', 'type' : 'text'},
            'estado' : {'title_th' : 'Estado', 'field' : 'estado', 'type' : 'active'},
            'aside' : {'title_th' : 'Aparece en aside', 'field' : 'aside', 'type' : 'active'},
            #'tipos' : {'title_th' : 'Contiene tipos', 'field' : 'tipos', 'type' : 'active'},
            'copy' : {'title_th' : 'Copiar', 'field' : 0, 'type' : 'action', 'action' : 'copy', 'mensaje' : 'Copiando Elemento'},
            'editar' : {'title_th' : 'Editar', 'field' : 'url_detalle', 'type' : 'link'},
            'subseccion' : {'title_th' : 'Modulos', 'field' : 'url_subseccion', 'type' : 'link'},
            'delete' : {'title_th' : 'Eliminar', 'field' : 'delete', 'type' : 'delete'},
        }

        # controlador de lista_class
        lista = lista_class(cls.metadata)

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
        url_detalle = url_final.copy()
        url_detalle.append('detail')
        # obtener unicamente elementos de la pagina actual
        respuesta = lista.get_row(class_name, where, condiciones, url_detalle)

        for value in respuesta['row']:
            value['url_subseccion'] = functions.generar_url(['modulo'], {class_name.idname :value[0]});
        
        menu = {'new' : True, 'excel' : False, 'regenerar' : false}

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
