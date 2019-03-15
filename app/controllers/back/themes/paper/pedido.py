from .base import base
from app.models.pedido import pedido as pedido_model

from app.models.table import table as table_model
from app.models.administrador import administrador as administrador_model
#from app.models.modulo import modulo as modulo_model
#from app.models.moduloconfiguracion import moduloconfiguracion as moduloconfiguracion_model
from app.models.pedidoestado import pedidoestado as pedidoestado_model
from app.models.pedidodireccion import pedidodireccion as pedidodireccion_model
from app.models.usuario import usuario as usuario_model
from app.models.usuariodireccion import usuariodireccion as usuariodireccion_model
from app.models.mediopago import mediopago as mediopago_model
from app.models.comuna import comuna as comuna_model
from app.models.region import region as region_model
from app.models.producto import producto as producto_model


from .detalle import detalle as detalle_class
from .lista import lista as lista_class
#from .head import head
#from .header import header
#from .aside import aside
#from .footer import footer

from core.app import app
#from core.database import database
from core.functions import functions
from core.image import image


import json

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



        if 'idpedidoestado' in configuracion['th']:
            pe           = pedidoestado_model.getAll()
            pedidoestado = {}
            for p in pe:
                pedidoestado[p[0]] = {'background' : p['color'], 'text' : p['titulo'],'color' : functions.getContrastColor(p['color'])}
            
            for v in respuesta['row']:
                v['idpedidoestado'] = pedidoestado[v['idpedidoestado']]
                

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
                    v['url_sub'] = functions.generar_url( [cls.sub], {class_name.idname: v[0]})

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













    @classmethod
    def detail(cls, var=[]):
        '''Controlador de detalle de elementos base, puede ser sobreescrito en el controlador de cada modulo'''
        ret = {'body': ''}
        # Clase para enviar a controlador de detalle
        class_name = cls.class_name
        get = app.get
        url_list = cls.url.copy()
        url_save = cls.url.copy()
        url_final = cls.url.copy()
        metadata=cls.metadata.copy()
        url_save.append('guardar')
        url_final.append('detail')
        if len(var)>0:
            id = int(var[0])
            url_final.append(id)
            metadata['title'] = 'Editar ' + metadata['title']
        else:
            id = 0
            metadata['title'] = 'Nuevo ' + metadata['title']

        cls.breadcrumb.append({'url': functions.generar_url( url_final), 'title': metadata['title'], 'active': 'active'})
        if cls.contiene_tipos and 'tipo' not in get:
            url_final = ['home']

        if not administrador_model.verificar_sesion():
            url_final = ['login', 'index'] + url_final
        # verificar sesion o redireccionar a login
        url_return = functions.url_redirect(url_final)
        if url_return != '':
            ret['error'] = 301
            ret['redirect'] = url_return
            return ret

        # cabeceras y campos que se muestran en el detalle:
        # titulo,campo de la tabla a usar, tipo (ver archivo detalle.py funcion "field")

        # controlador de detalle
        detalle = detalle_class(metadata)
        configuracion = detalle.configuracion(metadata['modulo'])
        
        if 'error' in configuracion:
            ret['error']=configuracion['error']
            ret['redirect']=configuracion['redirect']
            return ret

        row = class_name.getById(id) if id != 0 else []
        if cls.contiene_tipos:
            configuracion['campos']['tipo'] = { 'title_field': 'tipo', 'field': 'tipo', 'type': 'hidden', 'required': True}
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
            if 'idpadre' in configuracion['campos']:
                del configuracion['campos']['idpadre']

        if cls.class_parent != None:
            class_parent = cls.class_parent
            idparent = class_parent.idname

            is_array = True
            fields = table_model.getByname(class_name.table)
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

        if 'idusuario' in configuracion['campos']:
            if id == 0 or row['idusuario'] == 0:
                usuarios = usuario_model.getAll({}, {'order' : 'nombre ASC'})
                for u in usuarios:
                    u['titulo'] = u['nombre'] + ' (' + u['email'] + ')' + (  ': desactivado' if not u['estado'] else '')
                
                configuracion['campos']['idusuario']['parent'] = usuarios
            else:
                configuracion['campos']['idusuario']['type'] = 'hidden'





        if 'idpedidoestado' in configuracion['campos']:
            estados                                             = pedidoestado_model.getAll({'tipo' : get['tipo']})
            configuracion['campos']['idpedidoestado']['parent'] = estados
        if 'idmediopago' in configuracion['campos']:
            estados                                          = mediopago_model.getAll()
            configuracion['campos']['idmediopago']['parent'] = estados
        

        if 'cookie_pedido' in configuracion['campos'] and id != 0:
            configuracion['campos']['cookie_pedido']['type'] = 'text'
        





        if 'direcciones' in configuracion['campos']:
            com     = comuna_model.getAll()
            comunas = {}
            for c in com:
                if c['precio'] > 1:
                    r           = region_model.getById(c['idregion'])
                    c['precio'] = r['precio']
                comunas[c[0]] = c
            

            configuracion['campos']['direcciones']['direccion_entrega'] = []
            lista_productos                                             = producto_model.getAll({'tipo' : 1}, {'order' : 'titulo ASC'})
            for lp in lista_productos:
                portada               = image.portada(lp['foto'])
                thumb_url             = image.generar_url(portada, 'cart')
                lp = {'titulo' : lp['titulo'], 'idproducto' : lp['idproducto'], 'foto' : thumb_url, 'precio' : lp['precio_final'], 'stock' : lp['stock']}
            
            configuracion['campos']['direcciones']['lista_productos'] = lista_productos

            lista_atributos = producto_model.getAll({'tipo' : 2}, {'order' : 'titulo ASC'})
            for la in lista_productos:
                portada               = image.portada(la['foto'])
                thumb_url             = image.generar_url(portada, 'cart')
                la= {'titulo' : la['titulo'], 'idproducto' : la['idproducto'], 'foto' : thumb_url}
            
            configuracion['campos']['direcciones']['lista_atributos'] = lista_atributos

            if id != 0:
                if 'idusuario' in row and row['idusuario'] != '':
                    direcciones_entrega = usuariodireccion_model.getAll({'idusuario' : row['idusuario']})
                    for de  in direcciones_entrega:
                        de['precio'] = comunas[de['idcomuna']]['precio']
                        de['titulo'] = de['titulo'] + ' (' + de['direccion'] + ')'
                    
                    configuracion['campos']['direcciones']['direccion_entrega'] = direcciones_entrega
                

                pedidodirecciones         = pedidodireccion_model.getAll({'idpedido' : id})
                direcciones = []

                for d in pedidodirecciones:
                    new_d     = {'idpedidodireccion' : d['idpedidodireccion'], 'idusuariodireccion' : d['idusuariodireccion'], 'precio' : d['precio'], 'fecha_entrega' : d['fecha_entrega']}
                    prod      = pedidoproducto_model.getAll({'idpedido' : id, 'idpedidodireccion' : d[0]})
                    productos = {}
                    for p in prod:
                        portada     = image.portada(p['foto'])
                        thumb_url   = image.generar_url(portada, '')
                        new_p       = {'idpedidoproducto' : p['idpedidoproducto'], 'idproductoatributo' : p['idproductoatributo'], 'titulo' : p['titulo'], 'mensaje' : p['mensaje'], 'idproducto' : p['idproducto'], 'foto' : thumb_url, 'precio' : p['precio'], 'cantidad' : p['cantidad'], 'total' : p['total']}
                        productos.append(new_p)
                    
                    new_d['productos'] = productos
                    new_d['cantidad']  = count(productos)
                    if new_d['cantidad'] == 0:
                        new_d['cantidad'] = ''
                    

                    direcciones.append(new_d)
                
                row['direcciones'] = direcciones
                


        
        if 'fecha_pago' in row and row['fecha_pago']==0:
            row['fecha_pago']=''
        


        # informacion para generar la vista del detalle
        data = {
            'breadcrumb': cls.breadcrumb,
            'campos': configuracion['campos'],
            'row': row,
            'id': id if id != 0 else '',
            'current_url': functions.generar_url(url_final),
            'save_url': functions.generar_url(url_save),
            'list_url': functions.generar_url(url_list),
        }

        ret=detalle.normal(data)
        return ret






        
