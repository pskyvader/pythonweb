from .base import base
from app.models.pedido import pedido as pedido_model

#from app.models.table import table as table_model
from app.models.administrador import administrador as administrador_model
#from app.models.modulo import modulo as modulo_model
#from app.models.moduloconfiguracion import moduloconfiguracion as moduloconfiguracion_model
from app.models.pedidoestado import pedidoestado as pedidoestado_model

#from .detalle import detalle as detalle_class
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

class pedido(base):
    url = ['pedido']
    metadata = {'title' : 'pedido','modulo':'pedido'}
    breadcrumb = []
    def __init__(self):
        super().__init__(pedido_model)



    @classmethod
    def index(cls):
        '''Controlador de lista_class de elementos base, puede ser sobreescrito en el controlador de cada modulo'''
        ret = {'body': ''}
        # Clase para enviar a controlador de lista_class
        class_name = cls.class_name
        url_final=cls.url.copy()
        get = app.get
        if cls.contiene_tipos and not 'tipo' in get:
            url_final = ['home']
        if cls.contiene_hijos and not 'idpadre' in get:
            url_final = ['home']

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
        # controlador de lista_class
        lista = lista_class(cls.metadata)
        configuracion = lista.configuracion(cls.metadata['modulo'])
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

        if 'idpedidoestado' in get and get['idpedidoestado']!=0:
            where['idpedidoestado'] = get['idpedidoestado']
        
        condiciones = {'order' : 'fecha_pago DESC,fecha_creacion DESC'}
        url_detalle = url_final.copy()
        url_detalle.append('detail')
        # obtener unicamente elementos de la pagina actual
        respuesta = lista.get_row(class_name, where, condiciones, url_detalle)

        if 'copy' in configuracion['th']:
            configuracion['th']['copy']['action'] = configuracion['th']['copy']['field']
            configuracion['th']['copy']['field'] = 0
            configuracion['th']['copy']['mensaje'] = 'Copiando'



        if if 'idpedidoestado' in configuracion['th']:
            pe           = pedidoestado_model::getAll()
            pedidoestado = array()
            foreach (pe as key => p) {
                pedidoestado[p[0]] = array('background' => p['color'], 'text' => p['titulo'],'color' => functions::getContrastColor(p['color']))
            }

            foreach (respuesta['row'] as k => v) {
                respuesta['row'][k]['idpedidoestado'] = pedidoestado[v['idpedidoestado']]
            }
        }

        if cls.contiene_hijos:
            if cls.contiene_tipos:
                for v in respuesta['row']:
                    v['url_children'] = functions.generar_url(
                        url_final, {'idpadre': v[0], 'tipo': get['tipo']})

            else:
                for v in respuesta['row']:
                    v['url_children'] = functions.generar_url(
                        url_final, {'idpadre': v[0]})

        else:
            if 'url_children' in configuracion['th']:
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
            if 'url_sub' in configuracion['th']:
                del configuracion['th']['url_sub']

        # informacion para generar la vista de lista_class
        data = {
            'breadcrumb': cls.breadcrumb,
            'th': configuracion['th'],
            'current_url': functions.generar_url(url_final),
            'new_url': functions.generar_url(url_detalle),
        }

        data.update(respuesta)
        data.update(configuracion['menu'])
        ret = lista.normal(data)
        return ret










        if (this->contiene_hijos) {
            if (this->contiene_tipos) {
                foreach (respuesta['row'] as k => v) {
                    respuesta['row'][k]['url_children'] = functions::generar_url(this->url, array('idpadre' => v[0], 'tipo' => _GET['tipo']))
                }
            } else {
                foreach (respuesta['row'] as k => v) {
                    respuesta['row'][k]['url_children'] = functions::generar_url(this->url, array('idpadre' => v[0]))
                }
            }
        } else {
            unset(configuracion['th']['url_children'])
        }

        if (this->sub != '') {
            if (this->contiene_tipos) {
                foreach (respuesta['row'] as k => v) {
                    respuesta['row'][k]['url_sub'] = functions::generar_url(array(this->sub), array(class::idname => v[0], 'tipo' => _GET['tipo']))
                }
            } else {
                foreach (respuesta['row'] as k => v) {
                    respuesta['row'][k]['url_sub'] = functions::generar_url(array(this->sub), array(class::idname => v[0]))
                }
            }
        } else {
            unset(configuracion['th']['url_sub'])
        }

        data = array( //informacion para generar la vista de la lista, arrays SIEMPRE antes de otras variables!!!!
            'breadcrumb'  => this->breadcrumb,
            'th'          => configuracion['th'],
            'current_url' => functions::generar_url(this->url),
            'new_url'     => functions::generar_url(url_detalle),
        )
        data = array_merge(data, respuesta, configuracion['menu'])

        list->normal(data)
    }