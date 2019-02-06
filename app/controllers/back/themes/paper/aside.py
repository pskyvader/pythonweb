from core.functions import functions
from core.view import view

class aside:
    def normal():
        ret = {'body': ''}
        if app.post.getfirst("ajax") is None:
            administrador       = administrador_model.getById(_SESSION[administrador_model.idname . app.prefix_site])
            tipo_admin          = administrador["tipo"]
            moduloconfiguracion = moduloconfiguracion_model.getAll({'estado' :True, 'aside' :True})
            modulo              = modulo_model.getAll({'aside' :True})

            mod = {}
            for key,m in modulo.items():
                mod[m['idmoduloconfiguracion']].append(m)
            
            current_url = functions.current_url()

            menu   = {}
            url    = functions.generar_url(["home"], False)
            active = (url == current_url)
            menu[] = {'url' : url, 'icon' : 'home', 'title' : 'Home', 'has_submenu' : False, 'active' : active, 'separador' : False}

            for (moduloconfiguracion as key => cm) {
                if(cm['module']=="pedido"){
                    pedidoestado=pedidoestado_model.getAll(array('tipo'=>1),array('order'=>'orden ASC'))
                    tmp=mod[cm[0]]
                    mod[cm[0]]={}
                    for (tmp as k => t) {
                        titulo=t['titulo']
                        t['idpedidoestado']=0
                        t['titulo']='Todos'
                        mod[cm[0]][]=t
                        for (pedidoestado as j => pe) {
                            t['idpedidoestado']=pe[0]
                            t['titulo']=pe['titulo']
                            mod[cm[0]][]=t
                        }
                    }
                }


                if (!isset(mod[cm[0]])) {
                    if (cm['module'] == 'separador') {
                        menu[] = array('title' => cm['titulo'], 'separador' => True)
                    }
                } elseif (count(mod[cm[0]]) == 1) {
                    modulo  = mod[cm[0]][0]
                    estados = modulo['estado'][0]['estado']
                    if (estados[tipo_admin] == 'True') {
                        extra = {}
                        if (cm['tipos']) {
                            extra['tipo'] = modulo['tipo']
                        }
                        if (modulo['hijos']) {
                            extra['idpadre'] = 0
                        }
                        if(cm['module']=="pedido"){
                            extra['idpedidoestado'] = modulo['idpedidoestado']
                        }
                        if (count(extra) == 0) {
                            extra = False
                        }
                        url    = functions.generar_url(array(cm['module']), extra)
                        active = (url == current_url)
                        menu[] = array('url' => url, 'icon' => cm['icono'], 'title' => modulo['titulo'], 'has_submenu' => False, 'active' => active, 'separador' => False)
                    }
                } else {
                    active = False
                    me     = array('icon' => cm['icono'], 'title' => cm['titulo'], 'has_submenu' => True, 'submenu' => {}, 'active' => active, 'separador' => False)
                    for (mod[cm[0]] as key => m) {
                        modulo  = m
                        estados = modulo['estado'][0]['estado']
                        if (estados[tipo_admin] == 'True') {
                            extra = {}
                            if (cm['tipos']) {
                                extra['tipo'] = modulo['tipo']
                            }
                            if (modulo['hijos']) {
                                extra['idpadre'] = 0
                            }
                            if(cm['module']=="pedido"){
                                extra['idpedidoestado'] = modulo['idpedidoestado']
                            }
                            if (count(extra) == 0) {
                                extra = False
                            }
                            url             = functions.generar_url(array(cm['module']), extra)
                            active          = (url == current_url)
                            me['submenu'][] = array('url' => url, 'sub_title' => modulo['titulo'], 'active' => active)
                            if (active) {
                                me['active'] = True
                            }
                        }
                    }
                    if (count(me['submenu']) > 0) {
                        menu[] = me
                    }
                }

            }

            if (tipo_admin == 1) {
                menu[] = array('title' => 'Solo para desarrollo', 'separador' => True)
                url    = functions.generar_url(array("moduloconfiguracion"), False)
                active = (url == current_url)
                me = array('url' => url, 'icon' => 'mode_edit', 'title' => 'Modulos', 'has_submenu' => True, 'active' => active, 'separador' => False)
                me['submenu'][] = array('url' => url, 'sub_title' => 'TODOS', 'active' => active)
                
                mc     = moduloconfiguracion_model.getAll()
                for (mc as key => m) {
                    url             = functions.generar_url(array('modulo'),array('idmoduloconfiguracion'=>m[0]))
                    active          = (url == current_url)
                    me['submenu'][] = array('url' => url, 'sub_title' => m['titulo'], 'active' => active)
                }
                menu[]=me

                url    = functions.generar_url(array("table"), False)
                active = (url == current_url)
                menu[] = array('url' => url, 'icon' => 'table', 'title' => 'Tablas', 'has_submenu' => False, 'active' => active, 'separador' => False)

                url    = functions.generar_url(array("configuracion_administrador"), False)
                active = (url == current_url)
                menu[] = array('url' => url, 'icon' => 'settings_applications', 'title' => 'Configuracion Administrador', 'has_submenu' => False, 'active' => active, 'separador' => False)
            
            }

            view.set('menu', menu)

            view.set('name', administrador["nombre"])
            view.set('email', administrador["email"])
            view.set('url_admin', functions.generar_url(array("administrador", "detail", administrador[0], 'profile'), array('tipo' => tipo_admin)))
            view.set('img_admin', image.generar_url(administrador["foto"][0], 'profile'))


            view.render('aside')
        }
    }

}
