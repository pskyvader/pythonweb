from app.models.comuna import comuna as comuna_model
from app.models.pedido  import pedido as pedido_model
from app.models.pedidodireccion  import pedidodireccion as pedidodireccion_model
from app.models.pedidoproducto  import pedidoproducto as pedidoproducto_model
from app.models.producto  import producto as producto_model
from app.models.region  import region as region_model
from app.models.seo  import seo as seo_model
from app.models.usuario  import usuario as usuario_model
from app.models.usuariodireccion  import usuariodireccion as usuariodireccion_model

from core.app import app
from core.functions import functions
from core.image import image

import json

class order(base):
    steps = {
        1 : 'Paso 1: resumen del carro',
        2 : 'Paso 2: Direcciones',
        3 : 'Paso 3: Confirmación',
    }
    
    def __init__(self):
        super().__init__(app.idseo,False)
    
    def index(self):
        self.meta(self.seo)
        self.url.append('step')
        self.url.append('1')
        url_return = functions.url_redirect(self.url)
        if url_return != "":
            ret["error"] = 301
            ret["redirect"] = url_return
            return ret
    
    def step(self,var = []):
        error   = False
        mensaje = ''
        self.meta(self.seo)
        self.url.append('step')
        current_step = 1
        if 0 in var and var[0] in self.steps:
            current_step = var[0]
        
        self.url.append(current_step)
        logueado    = user.verificar(True)
        carro       = cart.current_cart(True)
        if not logueado['exito']:
            app.get['next_url'] = '/'.join(self.url)
            self.url        = ['cuenta', 'registro']
        
        if 2 == current_step:
            direcciones = usuariodireccion_model.getAll({'idusuario' : app.session[usuario_model.idname + app.prefix_site]})
            if len(direcciones) == 0:
                seo_usuario      = seo_model.getById(9)
                app.get['next_url'] = '/'.join(self.url)
                self.url        = [seo_usuario['url'], 'direccion']
            
        
        
        url_return = functions.url_redirect(self.url)
        if url_return != "":
            ret["error"] = 301
            ret["redirect"] = url_return
            return ret

        h = head(self.metadata)
        ret_head = h.normal()
        if ret_head["headers"] != "":
            return ret_head
        ret["body"] += ret_head["body"]

        he = header()
        ret["body"] += he.normal()["body"]


        ba = banner()
        ret["body"] += ba.individual(self.seo['banner'], self.metadata['title'], self.steps[current_step])["body"]

        if len(carro) == 0 or len(carro['productos']) == 0:
            mensaje = "Tu carro está vacío. Por favor agrega productos para continuar tu compra"
            error   = True
        

        if error:
            ret["body"].append(("order/error", {'mensaje':mensaje}))
        else:
            steps = self.steps(current_step, self.url)
            class_name = "step" + current_step
            data=self.class_name(carro, self.url)
            data['steps']=steps
            ret["body"].append(('order/' + current_step, data))
        

        f = footer()
        ret["body"] += f.normal()["body"]
        return ret
    
    @staticmethod
    def sidebar(carro):
        data={}
        data['subtotal']= carro['subtotal']
        data['total_direcciones']= carro['total_direcciones']
        data['total']= carro['total']
        return ('order/sidebar', data)

    @staticmethod
    def steps(current_step, url):
        steps = []
        for key,s in order.steps.items():
            active   = (current_step == key)
            disabled = (current_step < key)
            url_step = functions.generar_url([url[0], 'step', key])
            steps.append({'title' : s, 'active' : active, 'disabled' : disabled, 'url' : url_step})
        
        return view.render('order/steps', {'steps': steps})
    
    @staticmethod
    def step1(carro, url):
        attr = producto_model.getAll({'tipo':2}, {'order':'titulo ASC'})
        for lp in attr:
            portada    = image.portada(lp['foto'])
            thumb_url  = image.generar_url(portada, 'cart')
            lp = {'titulo' : lp['titulo'], 'idproducto' : lp['idproducto'], 'foto' : thumb_url}
        
        for p in carro['productos']:
            atributos = attr.copy()
            for a in atributos:
                if a['idproducto'] == p['idproductoatributo']:
                    a['selected'] = True
                else:
                    a['selected'] = False
            p['atributos'] = atributos
        
        sidebar = self.sidebar(carro)
        data=carro
        data['sidebar']=sidebar
        seo_producto = seo_model.getById(8)
        data['url_product']= functions.generar_url([seo_producto['url']])
        direcciones = usuariodireccion_model.getAll({'idusuario' : app.session[usuario_model.idname + app.prefix_site]})
        if len(direcciones) > 0:
            data['url_next']= functions.generar_url([url[0], 'step', 2])
        else:
            seo_usuario = seo_model.getById(9)
            data['url_next']= functions.generar_url([seo_usuario['url'], 'direccion'], {'next_url' : '/'.join([url[0], 'step', 2]) }  )
        
        return data
        
    

    @staticmethod
    def step2(carro:dict, url=list):
        """ Paso 2. NO AGREGAR ELEMENTOS AL CARRO antes de update_cart
        :type carro:dict:
        :param carro:dict:
    
        :type url:
        :param url:
    
        :raises:
    
        :rtype:
        """
        from datetime.datetime import strptime,strftime
        from datetime import timedelta


        horarios_entrega = {}
        hora_minima      = strptime("08:00", "%R")
        hora_maxima      = strptime("12:00", "%R")
        hora_corte       = strptime("18:00", "%R")
        hora_actual = hora_minima

        hora2 = (hora_actual + timedelta(hours=1)).strftime("%R")
        
        
        while strptime(hora2, "%R") < hora_maxima:
            hora1 = hora_actual.strftime("%R")
            hora2 = (hora_actual + timedelta(hours=1)).strftime("%R")

            horarios_entrega[hora1] = {'hora' : hora1, 'titulo' : hora1 + '  -   ' + hora2}
            hora_actual = (hora_actual + timedelta(minutes=15)).strftime("%R")



        fechas_bloqueadas   = []
        fechas_bloqueadas.append({'fecha' : '2019-01-22', 'texto' : 'Cerrado por Vacaciones'})
        fechas_bloqueadas.append({'fecha' : '2019-01-23', 'texto' : 'Cerrado por Vacaciones'})
        fechas_bloqueadas.append({'fecha' : '2019-01-24', 'texto' : 'Cerrado por Vacaciones'})

        if time() > hora_corte:
            fechas_bloqueadas.append({'fecha' : functions.formato_fecha(strtotime("+1 day"), '%F'), 'texto' : ''})
        

        fechas_especiales   = []
        fechas_especiales.append({'fecha' : '2019-02-14', 'texto' : 'Dia de los enamorados'})
        fechas_especiales.append({'fecha' : '2019-02-13', 'texto' : 'Dia de los enamorados'})

        comunas             = self.get_comunas()
        direcciones_entrega = usuariodireccion_model.getAll({'idusuario' : app.session[usuario_model.idname + app.prefix_site]})

        for de in direcciones_entrega:
            de['precio'] = comunas[de['idcomuna']]['precio']
            de['titulo'] = de['titulo'] + ' (' + de['direccion'] + " , " + comunas[de['idcomuna']]['titulo'] + ')'
        

        direcciones_pedido = pedidodireccion_model.getAll({'idpedido' : carro['idpedido']})
        if len(direcciones_pedido) == 0:
            du                        = direcciones_entrega[0]
            new_d                     = self.set_direccion(du, comunas)
            new_d['idpedido']         = carro['idpedido']
            new_d['idpedidoestado']   = 9 #pedido no pagado, porque esta en el carro
            new_d['cookie_direccion'] = carro['cookie_pedido'] + '-' + functions.generar_pass(2)

            pedidodireccion_model.insert(new_d)
            cart.update_cart(carro['idpedido'])
            carro              = cart.current_cart(True)
            direcciones_pedido = pedidodireccion_model.getAll({'idpedido' : carro['idpedido']})
        
        
        attr = producto_model.getAll({'tipo':2}, {'order':'titulo ASC'})
        atributos={}
        for at in attr:
            atributos[at[0]]=at
        
        iddireccion = direcciones_pedido[0][0]

        for p in carro['productos']:
            p['atributo'] = atributos[p['idproductoatributo']]['titulo']
            if 0 == p['idpedidodireccion']:
                update = {'id' : p['idpedidoproducto'], 'idpedidodireccion' : iddireccion}
                pedidoproducto_model.update(update)
                p['idpedidodireccion'] = iddireccion
            
        

        direcciones = []
        for dp in direcciones_pedido:
            lista_productos = []
            for p in carro['productos']:
                if p['idpedidodireccion'] == dp[0]:
                    lista_productos.append(p)
                    del p
            
            fecha_entrega = strptime(dp['fecha_entrega'], "%d/%m/%y")
            fecha_entrega = "" if fecha_entrega < functions.current_time(as_string=False) else functions.formato_fecha(fecha_entrega, '%F')

            hora_entrega = strptime(dp['fecha_entrega'], "%R")
            hora_entrega  = "" if hora_entrega < functions.current_time(as_string=False) else  functions.formato_fecha(hora_entrega, '%R')

            d= {
                'idpedidodireccion' : dp['idpedidodireccion'],
                'productos'         : lista_productos,
                'direccion_entrega' : direcciones_entrega,
                'fecha_entrega'     : fecha_entrega,
                'horarios_entrega'  : horarios_entrega,
                'precio'            : functions.formato_precio(dp['precio']),
            }

            for dir in d['direccion_entrega']:
                if dir[0] == dp['idusuariodireccion']:
                    dir['selected'] = True
                else:
                    dir['selected'] = False
                
            for h in d['horarios_entrega']:
                if hora_entrega == key:
                    h['selected'] = True
                else:
                    h['selected'] = False
                
            
            direcciones.append(d)
        

        sidebar = order.sidebar(carro)
        data={}

        data['direcciones']= direcciones
        data['fechas_bloqueadas']= json.dumps(fechas_bloqueadas)
        data['fechas_especiales']= json.dumps(fechas_especiales)
        data['sidebar']= sidebar

        seo_cuenta = seo_model.getById(9)
        data['url_direcciones']= functions.generar_url([seo_cuenta['url'], 'direcciones'], {'next_url' : '/'.join([url[0], 'step', 2]) } )

        seo_producto = seo_model.getById(8)
        data['url_product']= functions.generar_url([seo_producto['url']] )
        data['url_next']= functions.generar_url([url[0], 'step', 3])
        return data
    

    @staticmethod
    def step3(carro, url):
        from datetime.datetime import strptime
        sidebar   = order.sidebar(carro)
        atributos = producto_model.getAll({'tipo':2}, {'order':'titulo ASC'})
        for p in carro['productos']:
            p['mensaje'] =  p['mensaje'].replace("\n", "<br>\n")
            for a in atributos:
                if a['idproducto'] == p['idproductoatributo']:
                    p['atributo'] = a['titulo']
                    break

        comunas             = order.get_comunas()
        direcciones_entrega = usuariodireccion_model.getAll({'idusuario' : app.session[usuario_model.idname . app.prefix_site]})
        for de in direcciones_entrega:
            de['precio'] = comunas[de['idcomuna']]['precio']
            de['titulo'] = de['titulo'] + ' (' + de['direccion'] + " , " + comunas[de['idcomuna']]['titulo'] + ')'
        
        direcciones_pedido = pedidodireccion_model.getAll({'idpedido' : carro['idpedido']})

        direcciones = []
        for dp in direcciones_pedido:
            lista_productos = []
            for p in carro['productos']:
                if p['idpedidodireccion'] == dp[0]:
                    lista_productos.append(p)
                    del p
                
            fecha_entrega = strptime(dp['fecha_entrega'], "%d/%m/%y")
            fecha_entrega = "" if fecha_entrega < functions.current_time(as_string=False) else functions.formato_fecha(fecha_entrega, '%F')

            hora_entrega = strptime(dp['fecha_entrega'], "%R")
            hora_entrega  = "" if hora_entrega < functions.current_time(as_string=False) else  functions.formato_fecha(hora_entrega, '%R')

            for dir in direcciones_entrega:
                if dir[0] == dp['idusuariodireccion']:
                    direccion_entrega = dir['titulo']
                    break

            d = {
                'idpedidodireccion' : dp['idpedidodireccion'],
                'productos'         : lista_productos,
                'direccion_entrega' : direccion_entrega,
                'fecha_entrega'     : fecha_entrega,
                'hora_entrega'      : hora_entrega,
                'precio'            : functions.formato_precio(dp['precio']),
            }
            direcciones.append(d)
        


        data={}

        data['direcciones']= direcciones
        data['sidebar']= sidebar

        seo_cuenta = seo_model.getById(9)
        data['url_direcciones']= functions.generar_url([seo_cuenta['url'], 'direcciones'], {'next_url' : '/'.join([url[0], 'step', 2]) } )

        seo_producto = seo_model.getById(8)
        data['url_product']= functions.generar_url([seo_producto['url']] )
        data['url_next']= ''
        return data
    
    @staticmethod
    def set_direccion( direccion:dict,  comunas:dict):
        """ crea un array con la direccion para guardar en pedidodireccion
        :type direccion:dict:
        :param direccion:dict:
    
        :type comunas:dict:
        :param comunas:dict:
    
        :raises:
    
        :rtype:
        """
        new_d                       = {}
        new_d['idusuariodireccion'] = direccion[0]
        new_d['precio']             = direccion['precio']
        new_d['nombre']             = direccion['nombre']
        new_d['telefono']           = direccion['telefono']
        new_d['referencias']        = direccion['referencias']
        new_d['direccion_completa'] = direccion['direccion'] + ', ' + comunas[direccion['idcomuna']]['titulo']

        extra                       = ''
        extra += ', villa ' + direccion['villa'] if '' != direccion['villa'] else ''
        extra += ', edificio ' + direccion['edificio'] if '' != direccion['edificio'] else ''
        extra += ', departamento ' + direccion['departamento'] if '' != direccion['departamento'] else ''
        extra += ', condominio ' + direccion['condominio'] if '' != direccion['condominio'] else ''
        extra += ', casa ' + direccion['casa'] if '' != direccion['casa'] else ''
        extra += ', empresa ' + direccion['empresa'] if '' != direccion['empresa'] else ''

        if '' != extra:
            extra = extra[1:]
            new_d['direccion_completa'] += ';' + extra

        return new_d
    

    @staticmethod
    def get_comunas():
        """ retorna array de comunas con id como key, y precio
        :raises:
    
        :rtype:
        """
        com     = comuna_model.getAll()
        comunas = {}
        for c in com:
            if c['precio'] < 1:
                r           = region_model.getById(c['idregion'])
                c['precio'] = r['precio']
            comunas[c[0]] = c
        return comunas
    

    @staticmethod
    def change_productodireccion():
        """ cambia el mensaje en el producto correspondiente al pedido actual
            si el producto no corresponde al pedido, lanza error

        :param id:int: POST
        :param cantidad:int: POST

        :raises:
    
        :rtype: json
        """
        ret = {
            "headers": [("Content-Type", "application/json charset=utf-8")],
            "body": "",
        }
        respuesta = {'exito' : False, 'mensaje' : 'No has modificado un producto valido. Por favor recarga la pagina e intenta nuevamente'}
        campos    = app.post
        if 'id_final' in campos and 'idpedidoproducto' in campos :
            carro = cart.current_cart(True)
            if 'productos' in carro:
                for p in carro['productos']:
                    if p['idpedidoproducto'] == campos['idpedidoproducto']:
                        update             = {'id' : p['idpedidoproducto'], 'idpedidodireccion' : (campos['idfinal'])}
                        idpedidoproducto   = pedidoproducto_model.update(update)
                        respuesta['exito'] = True
                        break
                    
        ret["body"] = json.dumps(respuesta, ensure_ascii=False)
        return ret
    
    @staticmethod
    def change_direccion():
        """ cambia la direccion en el grupo de productos

        :param idusuariodireccion:int: POST
        :param idpedidodireccion:int: POST

        :raises:
    
        :rtype: json
        """
        ret = {
            "headers": [("Content-Type", "application/json charset=utf-8")],
            "body": "",
        }
        respuesta = {'exito' : False, 'mensaje' : 'No has modificado un producto valido. Por favor recarga la pagina e intenta nuevamente'}
        campos    = app.post
        if 'idusuariodireccion' in campos and 'idpedidodireccion' in campos:
            carro              = cart.current_cart(True)
            direcciones_pedido = pedidodireccion_model.getAll({'idpedido' : carro['idpedido']})
            comunas            = order.get_comunas()

            for d in direcciones_pedido:
                if d['idpedidodireccion'] == campos['idpedidodireccion']:
                    usuario_direccion           = usuariodireccion_model.getById(campos['idusuariodireccion'])
                    usuario_direccion['precio'] = comunas[usuario_direccion['idcomuna']]['precio']
                    update                      = order.set_direccion(usuario_direccion, comunas)
                    update['id']                = d['idpedidodireccion']
                    idpedidoproducto            = pedidodireccion_model.update(update)
                    respuesta['exito']          = True
                    respuesta['precio']         = usuario_direccion['precio']
                    break
                
            
        
        cart.update_cart(carro['idpedido'])
        
        ret["body"] = json.dumps(respuesta, ensure_ascii=False)
        return ret
    

    /**
     * change_fecha
     * cambia la fecha en el grupo de productos
     *
     * @param  POST idusuariodireccion
     * @param  POST fecha
     * @param  POST hora
     *
     * @return json
     */

    public static function change_fecha()
    
        respuesta = array('exito' : False, 'mensaje' : 'No has modificado una direccion valida. Por favor recarga la pagina e intenta nuevamente')
        campos    = functions.test_input(_POST)
        if isset(campos['idpedidodireccion']) and isset(campos['fecha']) and isset(campos['hora'])) 
            carro              = cart.current_cart(True)
            direcciones_pedido = pedidodireccion_model.getAll(array('idpedido' : carro['idpedido']))

            foreach (direcciones_pedido as key : d) 
                if d['idpedidodireccion'] == campos['idpedidodireccion']) 
                    update             = array('fecha_entrega' : campos['fecha'] . ' ' . campos['hora'])
                    update['id']       = d['idpedidodireccion']
                    idpedidoproducto   = pedidodireccion_model.update(update)
                    respuesta['exito'] = True
                    break
                
            
        
        echo json_encode(respuesta)
        exit
    

    /**
     * new_direccion
     * Crea un nuevo grupo de productos a un pedido
     *
     * @return json
     */
    public static function new_direccion(): json
    
        respuesta = array('exito' : False, 'mensaje' : 'No has modificado una direccion valida. Por favor recarga la pagina e intenta nuevamente')
        campos    = functions.test_input(_POST)
        carro     = cart.current_cart(True)

        comunas             = self.get_comunas()
        direcciones_entrega = usuariodireccion_model.getAll(array('idusuario' : app.session[usuario_model.idname . app.prefix_site]))
        foreach (direcciones_entrega as key : de) 
            direcciones_entrega[key]['precio'] = comunas[de['idcomuna']]['precio']
            direcciones_entrega[key]['titulo'] = de['titulo'] . ' (' . de['direccion'] . " , " . comunas[de['idcomuna']]['titulo'] . ')'
        

        du                        = reset(direcciones_entrega)
        new_d                     = self.set_direccion(du, comunas)
        new_d['idpedido']         = carro['idpedido']
        new_d['idpedidoestado']   = 9 //pedido no pagado, porque esta en el carro
        new_d['cookie_direccion'] = carro['cookie_pedido'] . '-' . functions.generar_pass(2)

        id_new                          = pedidodireccion_model.insert(new_d)
        id_direccion                    = du[0]
        respuesta['exito']              = True
        respuesta['idpedidodireccion']  = id_new
        respuesta['idusuariodireccion'] = id_direccion
        cart.update_cart(carro['idpedido'])

        echo json_encode(respuesta)
        exit
    

    /**
     * remove_direccion
     * quita una direccion del pedido
     *
     * @param  POST id
     *
     * @return json
     */
    public function remove_direccion(): json
    
        respuesta = array('exito' : False, 'mensaje' : '')
        campos    = functions.test_input(_POST)
        if not isset(campos['id'])) 
            respuesta['mensaje'] = 'No has seleccionado una direccion valida, por favor actualiza la pagina e intenta nuevamente'
            echo json_encode(respuesta)
            exit
        
        carro = cart.current_cart(True)

        direcciones_pedido = pedidodireccion_model.getAll(array('idpedido' : carro['idpedido']))

        foreach (direcciones_pedido as key : d) 
            if d['idpedidodireccion'] == campos['id']) 
                pedidodireccion_model.delete(d['idpedidodireccion'])
                respuesta['exito'] = True
                break
            
        

        cantidad = 0
        foreach (carro['productos'] as key : p) 
            if p['idpedidodireccion'] == campos['id']) 
                producto = producto_model.getById(p['idproducto'])
                if isset(producto['precio']) and producto['precio'] > 0) 
                    cantidad            = p['cantidad']
                    cantidad_final      = producto['stock'] + cantidad
                    actualizar_producto = array('id' : producto[0], 'stock' : cantidad_final)
                    producto_model.update(actualizar_producto)
                
                pedidoproducto_model.delete(p['idpedidoproducto'])
            
        

        cart.update_cart(carro['idpedido'])

        respuesta['mensaje'] = 'Direccion eliminada'
        respuesta['exito']   = True
        echo json_encode(respuesta)
        exit
    

    /**
     * crear_pedido
     * Modifica el estado del pedido actual. Esto elimina el carro actual.
     * actualiza el precio y los datos basicos del pedido
     * genera la url para ver el detalle del pedido y pagarlo
     *
     * @return json
     */
    public function crear_pedido(): json
    
        respuesta = array('exito' : False, 'mensaje' : '')
        carro     = cart.current_cart(True)
        if len(carro) == 0) 
            respuesta['mensaje'] = 'Tu pedido ya fue guardado, por favor ve a la seccion "Mis pedidos" en tu cuenta'
            echo json_encode(respuesta)
            exit
        else:
            attr      = producto_model.getAll({'tipo':2}, {'order':'titulo ASC'})
            atributos = array()
            foreach (attr as key : lp) 
                atributos[lp['idproducto']] = lp['titulo']
            
            foreach (carro['productos'] as key : p) 
                update = array('id' : p['idproducto'], 'titulo_atributo' : atributos[p['idproductoatributo']])
                pedidoproducto_model.update(update)
            
            update = array('idpedidoestado' : 3, 'id' : carro['idpedido']) //estado PAGO PENDIENTE
            pedido_model.update(update)
            cart.update_cart(carro['idpedido'])
            seo_cuenta         = seo_model.getById(9)
            url                = functions.generar_url(array(seo_cuenta['url'], 'pedido', carro['cookie_pedido']))
            respuesta['url']   = url
            respuesta['exito'] = True
            echo json_encode(respuesta)
            exit

        
    


