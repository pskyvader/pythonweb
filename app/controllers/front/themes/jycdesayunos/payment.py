from app.models.mediopago import mediopago as mediopago_model
from app.models.pedido import pedido as pedido_model
from app.models.pedidodireccion import pedidodireccion as pedidodireccion_model
from app.models.seo import seo as seo_model

from core.app import app
from core.functions import functions


from .head import head
from .header import header
from .banner import banner
from .breadcrumb import breadcrumb
from .footer import footer

class payment(base):
    cookie = ""
    configuration_webpay = None

    def __init__(self):
        super().__init__(app.idseo, False)
        # self.configuration_webpay = Configuration.forTestingWebpayPlusNormal()

    def index():
        seo_home = seo_model.getById(1)
        url_return = functions.url_redirect(seo_home["url"])
        if url_return != "":
            ret["error"] = 301
            ret["redirect"] = url_return
            return ret

    def verificar_medio_pago(self, cookie: str = "", idmedio: int = 0):

        """ comprueba si existe el medio de pago, sino vuelve al home
        :param cookie:str:
        :param idmedio:int:
    
        :raises:
    
        :rtype: mixed
        """
        medio_pago = None
        if "" != cookie:
            mp = mediopago_model.getById(idmedio)
            if "estado" in mp:
                cookie = functions.test_input(cookie)
                self.cookie = cookie
                self.url.append(cookie)
                medio_pago = mp
            else:
                seo_home = seo_model.getById(1)
                self.url = [seo_home["url"]]

        else:
            seo_home = seo_model.getById(1)
            self.url = [seo_home["url"]]

        return medio_pago

    def verificar_pedido(self,medio_pago:dict, render = True, pagado = False):
        """ comprueba si el pedido existe y es valido para pagos, sino devuelve mensaje de error
        :param medio_pago:dict:
        :param render:
        :param pagado:
    
        :raises:
    
        :rtype: tuple,list
        """    
        if render:
            h = head(self.metadata)
            ret_head = h.normal()
            if ret_head["headers"] != "":
                return ret_head
            ret["body"] += ret_head["body"]

            he = header()
            ret["body"] += he.normal()["body"]

            ba = banner()
            ret["body"] += ba.individual( self.seo["banner"], 'Pago via ' + medio_pago['titulo'], self.metadata['title'] )["body"]
            
        mensaje = ''
        if not medio_pago['estado']:
            mensaje = 'Medio de pago no disponible, Por favor intenta con otro medio de pago'
        else:
            pedido = pedido_model.getByCookie(self.cookie, False)
            if 'cookie_pedido' not in pedido:
                mensaje = 'Pedido no valido, Por favor ingresa a tu cuenta y selecciona un pedido valido'
            elif pagado:
                if 4 != pedido['idpedidoestado']:
                    mensaje = 'Este pedido no está pagado. Por favor intenta más tarde'
            elif 3 != pedido['idpedidoestado'] and 7 != pedido['idpedidoestado']:
                mensaje = 'Este pedido no se puede procesar, ya está pagado o aún no se ha completado.'
       
        if render and mensaje !='':
            return ('order/error',{'mensaje': mensaje})
        else:
            return pedido
            



    def update_pedido(self,pedido, medio_pago, idpedidoestado, fecha_pago = ''):
        lista_direcciones = pedidodireccion_model.getAll(array('idpedido' => pedido[0]));
        update_pedido     = array('id' => pedido[0], 'idpedidoestado' => idpedidoestado, 'idmediopago' => medio_pago[0]);
        if ('' != fecha_pago) {
            update_pedido['fecha_pago'] = fecha_pago;
        }
        pedido_model.update(update_pedido);
        foreach (lista_direcciones as key => direccion) {
            update_pedido = array('id' => direccion[0], 'idpedidoestado' => 9); // estado de direccion: pago pendiente
            if(idpedidoestado==4){
                update_pedido['idpedidoestado']=5; // estado de direccion: preparando producto
            }
            pedidodireccion_model.update(update_pedido);
        }
    }















    public function medio(var = array()):
        this->meta(this->seo);
        this->url[] = 'medio';
        idmedio     = -1;
        if (isset(var[0])) {
            idmedio     = functions.test_input(var[0]);
            this->url[] = idmedio;
        }
        medio_pago = this->verificar_medio_pago(var[1], idmedio);
        functions.url_redirect(this->url);

        pedido  = this->verificar_pedido(medio_pago);
        is_post = false;
        action  = '';
        form    = array();

        if (null != pedido) {
            if (2 == medio_pago[0]) { //  WEBPAY
                try {
                    transaction = (new Webpay(this->configuration_webpay))->getNormalTransaction();
                    amount      = pedido['total'];
                    // Identificador que será retornado en el callback de resultado:
                    sessionId = pedido['cookie_pedido'];
                    // Identificador único de orden de compra:
                    // buyOrder   = strval(rand(100000, 999999999));
                    buyOrder   = pedido['cookie_pedido'];
                    returnUrl  = functions.generar_url(array(this->url[0], 'process' . medio_pago[0], pedido['cookie_pedido']));
                    finalUrl   = functions.generar_url(array(this->url[0], 'pago' . medio_pago[0], pedido['cookie_pedido']));
                    initResult = transaction->initTransaction(amount, buyOrder, sessionId, returnUrl, finalUrl);

                    formAction = initResult->url;
                    tokenWs    = initResult->token;
                    is_post    = true;
                    action     = formAction;
                    form[]     = array('field' => 'token_ws', 'value' => tokenWs);
                } catch (\Exception e) {
                    mensaje = "Hubo un error al inicial el proceso webpay. Por favor intenta más tarde.";
                    if (error_reporting()) {
                        mensaje .= '<br/><br/><br/><br/>' . e;
                    }
                    view.set('mensaje', mensaje);
                    view.render('order/error');
                    pedido = null;
                }
            }
        }

        if (null != pedido) {
            seo_cuenta = seo_model.getById(9);
            view.set('title', medio_pago['titulo']);
            view.set('description', medio_pago['resumen']);
            view.set('is_post', is_post);
            view.set('action', action);
            view.set('form', form);
            view.set('url_back', functions.generar_url(array(seo_cuenta['url'], 'pedido', pedido['cookie_pedido'])));
            view.set('url_next', functions.generar_url(array(this->url[0], 'pago' . medio_pago[0], pedido['cookie_pedido'])));
            view.render('payment/resumen');
        }
        footer = new footer();
        footer->normal();
    }

    public function pago1(var = array()):
        this->meta(this->seo);
        this->url[] = 'pago1';
        idmedio     = 1;
        medio_pago  = this->verificar_medio_pago(var[0], idmedio);
        functions.url_redirect(this->url);

        pedido = this->verificar_pedido(medio_pago);
        if (null != pedido) {
            this->update_pedido(pedido, medio_pago, 10); // estado de pedido: esperando transferencia
            seo_cuenta                  = seo_model.getById(9);
            url_back                    = functions.generar_url(array(seo_cuenta['url'], 'pedido', pedido['cookie_pedido']));
            titulo                      = "Pedido " . pedido['cookie_pedido'] . " Esperando transferencia";
            cabecera                    = "Estimado " . pedido['nombre'] . ", " . medio_pago['descripcion'];
            campos                      = array();
            campos['Código de pedido'] = pedido['cookie_pedido'];
            campos['Estado del pedido'] = 'Esperando transferencia';
            campos['Medio de pago']     = medio_pago['titulo'];
            campos['Total del pedido']  = functions.formato_precio(pedido['total']);

            respuesta = self.email(pedido, titulo, cabecera, campos, url_back);

            view.set('title', medio_pago['titulo']);
            view.set('description', medio_pago['descripcion']);
            view.set('url_back', url_back);
            view.render('payment/confirmation');
        }
        footer = new footer();
        footer->normal();
    }

    public function process2(var = array()):
        error   = true;
        mensaje = '';
        campos  = functions.test_input(_POST);
        if (isset(campos['token_ws'])) {
            token = campos['token_ws'];

            transaction = (new Webpay(this->configuration_webpay))->getNormalTransaction();
            result      = transaction->getTransactionResult(token);
            output      = result->detailOutput;

            if (0 == output->responseCode) {
                idmedio    = 2;
                cookie     = output->buyOrder;
                medio_pago = this->verificar_medio_pago(cookie, idmedio);
                pedido     = this->verificar_pedido(medio_pago, false);
                if (null != pedido) {
                    this->update_pedido(pedido, medio_pago, 4, result->transactionDate); // estado de pedido: pagado
                    seo_cuenta                  = seo_model.getById(9);
                    url_back                    = functions.generar_url(array(seo_cuenta['url'], 'pedido', pedido['cookie_pedido']));
                    campos                      = array();
                    campos['Estado del pedido'] = 'Pagado';
                    campos['Medio de pago']     = medio_pago['titulo'];
                    campos['Código de pedido'] = pedido['cookie_pedido'];
                    campos['Total del pedido']  = functions.formato_precio(pedido['total']);

                    respuesta = self.email(pedido, '', '', campos, url_back);

                    view.set('action', result->urlRedirection);
                    form   = array();
                    form[] = array('field' => 'token_ws', 'value' => token);
                    view.set('form', form);
                    view.render('payment/post');
                    error      = false;
                } else {
                    mensaje = 'Este pedido no se puede procesar, ya está pagado o aún no se ha completado. Por favor intenta más tarde o selecciona otro medio de pago.';
                }
            } else {
                result->sessionId;
                result->transactionDate;
                result->urlRedirection;

                output->authorizationCode;
                output->responseCode;
                output->amount;
                output->buyOrder;
                mensaje = 'Hubo un error al procesar tu pago, por favor intenta más tarde o selecciona otro medio de pago.';
            }
        }

        if (error) {
            head = new head(this->metadata);
            head->normal();

            header = new header();
            header->normal();

            banner = new banner();
            banner->individual(this->seo['banner'], 'Pago via ' . medio_pago['titulo'], this->metadata['title']);
            view.set('mensaje', mensaje);
            view.render('order/error');
            footer = new footer();
            footer->normal();
        }
    }

    public function pago2(var = array()):
        this->meta(this->seo);
        this->url[] = 'pago2';
        idmedio     = 2;
        medio_pago = this->verificar_medio_pago(var[0], idmedio);
        functions.url_redirect(this->url);

        pedido = this->verificar_pedido(medio_pago, true, true);
        if (null != pedido) {
            seo_cuenta = seo_model.getById(9);
            url_back   = functions.generar_url(array(seo_cuenta['url'], 'pedido', pedido['cookie_pedido']));
            view.set('title', medio_pago['titulo']);
            view.set('description', medio_pago['descripcion']);
            view.set('url_back', url_back);
            view.render('payment/confirmation');
        }
        footer = new footer();
        footer->normal();
    }

    private static function email(pedido, titulo = '', cabecera = '', campos = array(), url_pedido):
        nombre_sitio  = app._title;
        config        = app.getConfig();
        email_empresa = config['main_email'];
        body_email    = array(
            'body'     => view.get_theme() . 'mail/pedido.html',
            'titulo'   => "Pedido " . pedido['cookie_pedido'] . " Pago realizado",
            'cabecera' => "Estimado " . pedido['nombre'] . ", aquí enviamos su información de pago. Si tiene alguna duda, no dude en contactarse con el centro de atención al cliente de " . nombre_sitio,
        );
        if ('' != cabecera) {
            body_email['cabecera'] = cabecera;
        }
        if ('' != titulo) {
            body_email['titulo'] = titulo;
        }
        body_email['campos_largos'] = array('' => 'Puedes ver el detalle de tu pedido <a href="' . url_pedido . '"><b>haciendo click aquí</b></a>');
        body_email['campos']        = campos;
        imagenes                    = array();
        adjuntos                    = array();
        body                        = email.body_email(body_email);
        respuesta                   = email.enviar_email(array(pedido['email'], email_empresa), body_email['titulo'], body, adjuntos, imagenes);
        return respuesta;
    }