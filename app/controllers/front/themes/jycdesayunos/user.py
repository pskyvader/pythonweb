from app.models.usuario import usuario as usuario_model

from .base import base

from core.app import app

class user(base):
    
    def __init__(self):
        super().__init__(app.idseo,False)


    def index(self):
        ret = {"body": []}
        self.meta(self.seo)
        verificar = self.verificar(True)
        if not verificar['exito']:
            self.url.append('login')
        

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
        ret["body"] += ba.individual(self.seo["banner"], self.metadata["title"])["body"]

        bc = breadcrumb()
        ret["body"] += bc.normal(self.breadcrumb)["body"]

        sidebar   = []
        sidebar.append({'title' : "Mis datos", 'active' : '', 'url' : functions.generar_url([self.url[0], 'datos'])})
        sidebar.append({'title' : "Mis direcciones", 'active' : '', 'url' : functions.generar_url([self.url[0], 'direcciones'])})
        sidebar.append({'title' : "Mis pedidos", 'active' : '', 'url' : functions.generar_url([self.url[0], 'pedidos'])})

        data={}
        data['sidebar']=('user/sidebar', {'sidebar_user': sidebar})
        ret["body"].append(('user/detail',data))
        
        f = footer()
        ret["body"] += f.normal()["body"]
        return ret

    def datos(self):
        from time import time
        ret = {"body": []}
        self.meta(self.seo)
        verificar = self.verificar(True)
        if verificar['exito']:
            self.url.append('datos')
        else:
            self.url.append('login')


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
        ret["body"] += ba.individual(self.seo["banner"], self.metadata["title"],'Mis datos')["body"]

        bc = breadcrumb()
        ret["body"] += bc.normal(self.breadcrumb)["body"]
        

        sidebar   = []
        sidebar.append({'title' : "Mis datos", 'active' : 'active', 'url' : functions.generar_url([self.url[0], 'datos'])})
        sidebar.append({'title' : "Mis direcciones", 'active' : '', 'url' : functions.generar_url([self.url[0], 'direcciones'])})
        sidebar.append({'title' : "Mis pedidos", 'active' : '', 'url' : functions.generar_url([self.url[0], 'pedidos'])})



        data={}
        data['sidebar']=('user/sidebar', {'sidebar_user': sidebar})
        ret["body"].append(('user/detail',data.copy()))
        
        
        data={}
        usuario= usuario_model.getById(app.session[usuario_model.idname + app.prefix_site])
        data['nombre']= usuario['nombre']
        data['telefono']=usuario['telefono']
        data['email']=usuario['email']
        token = functions.generar_pass(20)
        app.session['datos_token'] = {'token' : token, 'time' : time()}
        data['token']= token
        ret["body"].append(('user/datos',data.copy()))
        
        f = footer()
        ret["body"] += f.normal()["body"]
        return ret


        
    /**
     * datos_process
     * procesa el POST para modificacion de datos
     *
     * @return json
     * 
     */
    public function datos_process()
    {
        respuesta = array('exito' : false, 'mensaje' : '')
        verificar = self.verificar(True)
        if(!verificar['exito']){
            respuesta['mensaje']='Debes ingresar a tu cuenta'
            return respuesta
        }
        campos    = functions.test_input(_POST['campos'])

        if isset(campos['nombre']) && isset(campos['telefono']) && isset(campos['email']) && isset(campos['token']):
            if isset(app.session['datos_token']['token']) && app.session['datos_token']['token'] == campos['token']:
                if time() - app.session['datos_token']['time'] <= 120:
                    datos=array(
                        'nombre':campos['nombre'],
                        'telefono':campos['telefono'],
                        'email':campos['email'],
                        'pass':(isset(campos['pass']) && campos['pass']!='')?campos['pass']:'',
                        'pass_repetir':(isset(campos['pass_repetir']) && campos['pass_repetir']!='')?campos['pass_repetir']:'',
                    )
                    respuesta = usuario_model.actualizar(datos)
                    if respuesta['exito']:
                        respuesta['mensaje'] = "Datos modificados correctamente"
                    }
                else:
                    respuesta['mensaje'] = 'Error de token, recarga la pagina e intenta nuevamente'
                }
            else:
                respuesta['mensaje'] = 'Error de token, recarga la pagina e intenta nuevamente'
            }
        else:
            respuesta['mensaje'] = 'Debes llenar los campos obligatorios'
        }

        echo json_encode(respuesta)
    }

    /**
     * lista de direcciones
     *
     * @return void
     */
    public function direcciones(){
        self.meta(self.seo)
        verificar = self.verificar(True)
        if verificar['exito']:
            self.url[] = 'direcciones'
        else:
            self.url[] = 'login'
        }
        functions.url_redirect(self.url)

        head = new head(self.metadata)
        head->normal()

        header = new header()
        header->normal()

        banner = new banner()
        banner->individual(self.seo['banner'], self.metadata['title'],'Mis Direcciones')
        sidebar   = array()
        sidebar[] = array('title' : "Mis datos", 'active' : '', 'url' : functions.generar_url(array(self.url[0], 'datos')))
        sidebar[] = array('title' : "Mis direcciones", 'active' : 'active', 'url' : functions.generar_url(array(self.url[0], 'direcciones')))
        sidebar[] = array('title' : "Mis pedidos", 'active' : '', 'url' : functions.generar_url(array(self.url[0], 'pedidos')))

        view.set('sidebar_user', sidebar)
        sidebar=view.render('user/sidebar', false, True)
        view.set('sidebar',sidebar)
        dir=usuariodireccion_model.getAll(array('idusuario':app.session[usuario_model.idname . app.prefix_site]))
        direcciones=array()
        foreach (dir as key : d:
            direcciones[]=array(
                'title':d['titulo'],
                'nombre':d['nombre'],
                'direccion':d['direccion'],
                'telefono':d['telefono'],
                'url':functions.generar_url(array(self.url[0], 'direccion',d[0]))
            )
        }
        view.set('direcciones',direcciones)
        view.set('url_new',functions.generar_url(array(self.url[0], 'direccion')))
        
        view.render('user/direcciones-lista')

        footer = new footer()
        footer->normal()
    }


    /**
     * modificar o crear direccion
     *
     * @param  mixed var
     *
     * @return void
     */
    public function direccion(var=array()){
        self.meta(self.seo)
        verificar = self.verificar(True)
        if verificar['exito']:
            if(isset(var[0])){
                direccion=usuariodireccion_model.getById(var[0])
                if(direccion['idusuario']==app.session[usuario_model.idname . app.prefix_site]){
                    self.url[] = 'direccion'
                    self.url[] = var[0]
                }else{
                    self.url[] = 'direcciones'
                }
            }else{
                self.url[] = 'direccion'
            }
        else:
            self.url[] = 'login'
        }
        functions.url_redirect(self.url)

        head = new head(self.metadata)
        head->normal()

        header = new header()
        header->normal()

        banner = new banner()
        banner->individual(self.seo['banner'], self.metadata['title'],'Modificar dirección')
        sidebar   = array()
        sidebar[] = array('title' : "Mis datos", 'active' : '', 'url' : functions.generar_url(array(self.url[0], 'datos')))
        sidebar[] = array('title' : "Mis direcciones", 'active' : 'active', 'url' : functions.generar_url(array(self.url[0], 'direcciones')))
        sidebar[] = array('title' : "Mis pedidos", 'active' : '', 'url' : functions.generar_url(array(self.url[0], 'pedidos')))

        view.set('sidebar_user', sidebar)
        sidebar=view.render('user/sidebar', false, True)
        view.set('sidebar',sidebar)

        moduloconfiguracion = moduloconfiguracion_model.getByModulo('usuariodireccion')
        if isset(moduloconfiguracion[0]):
            modulo= modulo_model.getAll(array('idmoduloconfiguracion' : moduloconfiguracion[0], 'tipo' :1))
            modulo=modulo[0]['detalle']
        }else{
            modulo=array()
        }


        com=comuna_model.getAll(array(),array('order':'titulo ASC'))
        comunas=array()
        foreach (com as key : c:
            comunas[]=array('title':c['titulo'],'value':c[0],'selected':(isset(direccion) && direccion['idcomuna']==c[0]))
        }

        campos_requeridos=array()
        campos_opcionales=array()
        foreach (modulo as key : m:
            if(in_array(True,m['estado'])){
                unset(m['estado'])
                if(m['field']=='idcomuna'){
                    m['options']=comunas
                }else{
                    m['value']=(isset(direccion))?direccion[m['field']]:''
                }
                m['is_text']=(m['tipo']=='text')
                if(m['required']){
                    campos_requeridos[]=m
                }else{
                    campos_opcionales[]=m
                }
            }
        }
        view.set('campos_requeridos',campos_requeridos)
        view.set('campos_opcionales',campos_opcionales)
        view.set('title',isset(direccion)?direccion['titulo']:'Nueva dirección')
        view.set('id',isset(direccion)?direccion[0]:'')


        
        token                      = sha1(uniqid(microtime(), True))
        app.session['direccion_token'] = array('token' : token, 'time' : time())
        view.set('token', token)

        view.render('user/direcciones-detalle')

        footer = new footer()
        footer->normal()
    }

    
    /**
     * direccion_process
     * procesa el POST para modificacion de direccion
     *
     * @return json
     * 
     */
    public function direccion_process()
    {
        respuesta = array('exito' : false, 'mensaje' : '')
        verificar = self.verificar(True)
        if(!verificar['exito']){
            respuesta['mensaje']='Debes ingresar a tu cuenta'
            return respuesta
        }
        campos    = functions.test_input(_POST['campos'])

        if isset(campos['token']) && isset(campos['id']):
            if isset(app.session['direccion_token']['token']) && app.session['direccion_token']['token'] == campos['token']:
                if time() - app.session['direccion_token']['time'] <= 360:
                    unset(campos['token'])
                    campos['idusuario']=app.session[usuario_model.idname . app.prefix_site]
                    campos['tipo']=1
                    if(campos['id']!=''){
                        respuesta['exito'] = usuariodireccion_model.update(campos)
                    }else{
                        respuesta['exito'] = usuariodireccion_model.insert(campos)
                    }
                    if respuesta['exito']:
                        respuesta['mensaje'] = "Direccion guardada correctamente"
                        
                        if(isset(_GET['next_url'])){
                            respuesta['next_url'] = _GET['next_url']
                        }
                    }else{
                        respuesta['mensaje'] = "Hubo un error al guardar la direccion, comprueba los campos obligatorios e intentalo nuevamente"
                    }
                else:
                    respuesta['mensaje'] = 'Error de token, recarga la pagina e intenta nuevamente'
                }
            else:
                respuesta['mensaje'] = 'Error de token, recarga la pagina e intenta nuevamente'
            }
        else:
            respuesta['mensaje'] = 'Debes llenar los campos obligatorios'
        }

        echo json_encode(respuesta)
    }



    
    /**
     * lista de pedidos
     *
     * @return void
     */
    public function pedidos(){
        self.meta(self.seo)
        verificar = self.verificar(True)
        if verificar['exito']:
            self.url[] = 'pedidos'
        else:
            self.url[] = 'login'
        }
        functions.url_redirect(self.url)

        head = new head(self.metadata)
        head->normal()

        header = new header()
        header->normal()

        banner = new banner()
        banner->individual(self.seo['banner'], self.metadata['title'],'Mis Pedidos')
        sidebar   = array()
        sidebar[] = array('title' : "Mis datos", 'active' : '', 'url' : functions.generar_url(array(self.url[0], 'datos')))
        sidebar[] = array('title' : "Mis direcciones", 'active' : '', 'url' : functions.generar_url(array(self.url[0], 'direcciones')))
        sidebar[] = array('title' : "Mis pedidos", 'active' : 'active', 'url' : functions.generar_url(array(self.url[0], 'pedidos')))

        view.set('sidebar_user', sidebar)
        sidebar=view.render('user/sidebar', false, True)
        view.set('sidebar',sidebar)
        ep=pedidoestado_model.getAll(array('tipo':1))
        estados_pedido=array()
        foreach (ep as key : e:
            estados_pedido[e[0]]=e
        }


        usuario= usuario_model.getById(app.session[usuario_model.idname . app.prefix_site])
        pedidos=pedido_model.getByIdusuario(usuario[0],false)//obtiene todos los pedidos del usuario actual, con cualquier estado del pedido
        foreach (pedidos as key : p:
            if(p['idpedidoestado']==1){ //Quita cualquier pedido que este en carro
                unset(pedidos[key])
            }else{
                pedidos[key]['total']=functions.formato_precio(p['total'])
                pedidos[key]['fecha']=(p['fecha_pago']!=0)?p['fecha_pago']:p['fecha_creacion']
                pedidos[key]['url']=functions.generar_url(array(self.url[0], 'pedido',p['cookie_pedido']))
                pedidos[key]['estado']=estados_pedido[p['idpedidoestado']]['titulo']
                pedidos[key]['background_estado']=estados_pedido[p['idpedidoestado']]['color']
                pedidos[key]['color_estado']=functions.getContrastColor(estados_pedido[p['idpedidoestado']]['color'])
            }
        }
        view.set('pedidos',pedidos)        
        view.render('user/pedidos-lista')

        footer = new footer()
        footer->normal()
    }


   /**
     * Ver o pagar pedido
     *
     * @param  array var
     *
     * @return void
     */
    public function pedido(var=array()){
        self.meta(self.seo)
        verificar = self.verificar(True)
        if verificar['exito']:
            if(isset(var[0])){
                pedido=pedido_model.getByCookie(var[0],false)
                //Podria desaparecer si se necesita que cualquier pedido sea publico
                if(isset(pedido['idusuario']) && pedido['idusuario']==app.session[usuario_model.idname . app.prefix_site]){
                    self.url[] = 'pedido'
                    self.url[] = var[0]
                }else{
                //Podria desaparecer si se necesita que cualquier pedido sea publico
                    self.url[] = 'pedidos'
                }
            }else{
                self.url[] = 'pedido'
            }
        else:
            self.url[] = 'login'
        }
        functions.url_redirect(self.url)

        head = new head(self.metadata)
        head->normal()

        header = new header()
        header->normal()

        banner = new banner()
        banner->individual(self.seo['banner'], self.metadata['title'],'Detalle del pedido')
        sidebar   = array()
        sidebar[] = array('title' : "Mis datos", 'active' : '', 'url' : functions.generar_url(array(self.url[0], 'datos')))
        sidebar[] = array('title' : "Mis direcciones", 'active' : '', 'url' : functions.generar_url(array(self.url[0], 'direcciones')))
        sidebar[] = array('title' : "Mis pedidos", 'active' : 'active', 'url' : functions.generar_url(array(self.url[0], 'pedidos')))

        view.set('sidebar_user', sidebar)
        sidebar=view.render('user/sidebar', false, True)

        ep=pedidoestado_model.getAll()
        estados_pedido=array()
        foreach (ep as key : e:
            estados_pedido[e[0]]=e
        }
        direcciones_pedido = pedidodireccion_model.getAll(array('idpedido' : pedido['idpedido']))
        productos_pedido=pedidoproducto_model.getAll(array('idpedido' : pedido['idpedido']))
        foreach (direcciones_pedido as key : dp:
            direcciones_pedido[key]['precio']=functions.formato_precio(dp['precio'])
            direcciones_pedido[key]['estado']=estados_pedido[dp['idpedidoestado']]['titulo']
            direcciones_pedido[key]['background_estado']=estados_pedido[dp['idpedidoestado']]['color']
            direcciones_pedido[key]['color_estado']=functions.getContrastColor(estados_pedido[dp['idpedidoestado']]['color'])
            lista_productos = array()
            foreach (productos_pedido as k : p:
                if p['idpedidodireccion'] == dp[0]:
                    portada      = image.portada(p['foto'])
                    thumb_url    = image.generar_url(portada, '')
                    p['total']=functions.formato_precio(p['total'])
                    p['foto']=thumb_url
                    lista_productos[] = p
                    unset(productos_pedido[k])
                }
            }
            direcciones_pedido[key]['lista_productos']=lista_productos
        }
        pedido['total']=functions.formato_precio(pedido['total'])
        pedido['direcciones_pedido']=direcciones_pedido
        pedido['estado']=estados_pedido[pedido['idpedidoestado']]['titulo']
        pedido['background_estado']=estados_pedido[pedido['idpedidoestado']]['color']
        pedido['color_estado']=functions.getContrastColor(estados_pedido[pedido['idpedidoestado']]['color'])

        view.set_array(pedido)
        view.set('sidebar',sidebar)

        medios_pago=array()
        descripcion_pago=''
        if(pedido['idpedidoestado']==3 || pedido['idpedidoestado']==7){ // Solo si hay pago pendiente
            medios_pago=mediopago_model.getAll()
            seo_pago=seo_model.getById(12) //seo medios de pago
            foreach (medios_pago as key : mp:
                url=functions.generar_url(array(seo_pago['url'],'medio',mp[0],pedido['cookie_pedido']))
                medios_pago[key]['url']=url
            }
        }else{
            medio_pago=mediopago_model.getById(pedido['idmediopago'])
            descripcion_pago=medio_pago['descripcion']
        }
        view.set('medios_pago',medios_pago)
        view.set('descripcion_pago',descripcion_pago)
        view.set('is_descripcion_pago',(trim(strip_tags(descripcion_pago))!=''))
        view.set('pago',(count(medios_pago)>0) )

        view.render('user/pedidos-detalle')

        footer = new footer()
        footer->normal()
    }








    public function registro()
    {
        self.meta(self.seo)
        
        verificar = self.verificar(True)
        if(verificar['exito']){
            if(isset(_GET['next_url'])){
                self.url = explode('/',_GET['next_url'])
            }else{
                self.url[] = 'datos'
            }
        }else{
            self.url[] = 'registro'
        }
        functions.url_redirect(self.url)

        head = new head(self.metadata)
        head->normal()

        header = new header()
        header->normal()

        banner = new banner()
        banner->individual(self.seo['banner'], 'Registro')

        token                      = sha1(uniqid(microtime(), True))
        app.session['registro_token'] = array('token' : token, 'time' : time())
        view.set('token', token)
        view.set('url_login', functions.generar_url(array(self.url[0], 'login')))
        view.render('user/registro')

        footer = new footer()
        footer->normal()
    }
    
    /**
     * registro_process
     * procesa el POST para registro
     *
     * @return json
     * 
     */
    public function registro_process()
    {
        respuesta = array('exito' : false, 'mensaje' : '')
        campos    = functions.test_input(_POST['campos'])

        if isset(campos['nombre']) && isset(campos['telefono']) && isset(campos['email']) && isset(campos['pass']) && isset(campos['pass_repetir']) && isset(campos['token']):
            if isset(app.session['registro_token']['token']) && app.session['registro_token']['token'] == campos['token']:
                if time() - app.session['registro_token']['time'] <= 120:
                    respuesta = usuario_model.registro(campos['nombre'], campos['telefono'], campos['email'], campos['pass'], campos['pass_repetir'])
                    if respuesta['exito']:
                        respuesta['exito'] = usuario_model.login(campos['email'], campos['pass'], isset(campos['recordar']))
                        if not respuesta['exito']:
                            respuesta['mensaje'] = "Cuenta creada correctamente, pero ha ocurrido un error al ingresar. Intenta loguearte"
                        else:
                            respuesta['mensaje'] = "Bienvenido"
                        }
                    }
                else:
                    respuesta['mensaje'] = 'Error de token, recarga la pagina e intenta nuevamente'
                }
            else:
                respuesta['mensaje'] = 'Error de token, recarga la pagina e intenta nuevamente'
            }
        else:
            respuesta['mensaje'] = 'Debes llenar todos los campos'
        }

        echo json_encode(respuesta)
    }
    public function recuperar(){
        self.meta(self.seo)
        self.url[] = 'recuperar'
        functions.url_redirect(self.url)

        head = new head(self.metadata)
        head->normal()

        header = new header()
        header->normal()

        banner = new banner()
        banner->individual(self.seo['banner'], 'Recuperar contraseña')

        token                   = sha1(uniqid(microtime(), True))
        app.session['recuperar_token'] = array('token' : token, 'time' : time())
        view.set('token', token)
        view.set('url_registro', functions.generar_url(array(self.url[0], 'registro')))
        view.render('user/recuperar')

        footer = new footer()
        footer->normal()

    }
    
    /**
     * recuperar_process
     * procesa el POST para recuperacion de contraseña
     *
     * @return json
     * 
     */
    public function recuperar_process()
    {
        respuesta = array('exito' : false, 'mensaje' : '')
        campos    = functions.test_input(_POST['campos'])

        if(isset(campos['email']) && isset(campos['token'])){
            if(app.session['recuperar_token']['token']==campos['token']){
                if(time()-app.session['recuperar_token']['time']<=120){
                    respuesta=usuario_model.recuperar(campos['email'])
                    if(respuesta["exito"]){
                        respuesta['mensaje'] = "Se ha enviado tu nueva contraseña a tu email. recuerda modificarla al ingresar."
                    }
                }else{
                    respuesta['mensaje'] = 'Error de token, recarga la pagina e intenta nuevamente'
                }
            }else{
                respuesta['mensaje'] = 'Error de token, recarga la pagina e intenta nuevamente'
            }
        }else{
            respuesta['mensaje'] = 'Debes llenar todos los campos'
        }

        echo json_encode(respuesta)
    }
    public function login()
    {
        self.meta(self.seo)
        verificar = self.verificar(True)
        if(verificar['exito']){
            if(isset(_GET['next_url'])){
                self.url = explode('/',_GET['next_url'])
            }else{
                self.url[] = 'datos'
            }
        }else{
            self.url[] = 'login'
        }
        functions.url_redirect(self.url)

        head = new head(self.metadata)
        head->normal()

        header = new header()
        header->normal()

        banner = new banner()
        banner->individual(self.seo['banner'], 'Login')

        token                   = sha1(uniqid(microtime(), True))
        app.session['login_token'] = array('token' : token, 'time' : time())
        view.set('token', token)
        view.set('url_recuperar', functions.generar_url(array(self.url[0], 'recuperar')))
        view.set('url_registro', functions.generar_url(array(self.url[0], 'registro')))
        view.render('user/login')

        footer = new footer()
        footer->normal()
    }
    
    /**
     * login_process
     * procesa el POST para login
     *
     * @return json
     * 
     */
    public function login_process()
    {
        respuesta = array('exito' : false, 'mensaje' : '')
        campos    = functions.test_input(_POST['campos'])

        if isset(campos['email']) && isset(campos['pass']) && isset(campos['token']):
            if isset(app.session['login_token']['token']) && app.session['login_token']['token'] == campos['token']:
                if time() - app.session['login_token']['time'] <= 120:
                    respuesta['exito'] = usuario_model.login(campos['email'], campos['pass'], isset(campos['recordar']))
                    if not respuesta['exito']:
                        respuesta['mensaje'] = "Ha ocurrido un error al ingresar. Revisa tus datos e intenta nuevamente"
                    else:
                        respuesta['mensaje'] = "Bienvenido"
                        if(isset(_GET['next_url'])){
                            respuesta['next_url'] = _GET['next_url']
                        }
                    }
                else:
                    respuesta['mensaje'] = 'Error de token, recarga la pagina e intenta nuevamente'.(time() - app.session['login_token']['time'])
                }
            else:
                respuesta['mensaje'] = 'Error de token, recarga la pagina e intenta nuevamente'
            }
        else:
            respuesta['mensaje'] = 'Debes llenar todos los campos'
        }

        echo json_encode(respuesta)
    }
    /**
     * verificar
     *
     * @param  mixed return
     *
     * @return array o json
     */
    public static function verificar(bool return = false)
    {
        respuesta   = array('exito' : false, 'mensaje' : '')
        logueado    = usuario_model.verificar_sesion()
        if not logueado:
            if isset(_COOKIE['cookieusuario' . app.prefix_site]):
                logueado = usuario_model.login_cookie(_COOKIE['cookieusuario' . app.prefix_site])
            }
        }
        respuesta['exito'] = logueado
        if logueado:
            nombre               = explode(" ", app.session['nombreusuario' . app.prefix_site])
            respuesta['mensaje'] = nombre[0]
        }
        if return:
            return respuesta
        else:
            echo json_encode(respuesta)
        }
    }
    public function logout()
    {
        usuario_model.logout()
        echo json_encode(array('exito' : True, 'mensaje' : 'Gracias por visitar nuestro sitio'))
    }