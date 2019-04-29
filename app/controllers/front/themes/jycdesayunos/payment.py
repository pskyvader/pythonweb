from app.models.mediopago import mediopago as mediopago_model
from app.models.pedido import pedido as pedido_model
from app.models.pedidodireccion import pedidodireccion as pedidodireccion_model
from app.models.seo import seo as seo_model

from core.app import app
from core.functions import functions

from .base import base

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
                cookie = functions.remove_tags(cookie)
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

    def verificar_pedido(self, medio_pago: dict, pagado=False):
        """ comprueba si el pedido existe y es valido para pagos, sino devuelve mensaje de error
        :param medio_pago:dict:
        :param render:
        :param pagado:
    
        :raises:
    
        :rtype: tuple,list
        """
        mensaje = ""
        if not medio_pago["estado"]:
            mensaje = (
                "Medio de pago no disponible, Por favor intenta con otro medio de pago"
            )
        else:
            pedido = pedido_model.getByCookie(self.cookie, False)
            if "cookie_pedido" not in pedido:
                mensaje = "Pedido no valido, Por favor ingresa a tu cuenta y selecciona un pedido valido"
            elif pagado:
                if 4 != pedido["idpedidoestado"]:
                    mensaje = "Este pedido no está pagado. Por favor intenta más tarde"
            elif 3 != pedido["idpedidoestado"] and 7 != pedido["idpedidoestado"]:
                mensaje = "Este pedido no se puede procesar, ya está pagado o aún no se ha completado."

        if mensaje != "":
            return ("order/error", {"mensaje": mensaje})
        else:
            return pedido

    def update_pedido(self, pedido, medio_pago, idpedidoestado, fecha_pago=""):
        lista_direcciones = pedidodireccion_model.getAll({"idpedido": pedido[0]})
        update_pedido = {
            "id": pedido[0],
            "idpedidoestado": idpedidoestado,
            "idmediopago": medio_pago[0],
        }
        if "" != fecha_pago:
            update_pedido["fecha_pago"] = fecha_pago

        pedido_model.update(update_pedido)
        for direccion in lista_direcciones:
            update_pedido = {
                "id": direccion[0],
                "idpedidoestado": 9,
            }  # estado de direccion: pago pendiente
            if idpedidoestado == 4:
                update_pedido[
                    "idpedidoestado"
                ] = 5  # estado de direccion: preparando producto

            pedidodireccion_model.update(update_pedido)

    def medio(self, var=[]):
        ret = {"body": []}
        self.meta(self.seo)
        self.url.append("medio")
        idmedio = -1
        if len(var) > 0:
            idmedio = int(var[0])
            self.url.append(idmedio)

        medio_pago = self.verificar_medio_pago(var[1], idmedio)

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
        ret["body"] += ba.individual(
            self.seo["banner"],
            "Pago via " + medio_pago["titulo"],
            self.metadata["title"],
        )["body"]

        pedido = self.verificar_pedido(medio_pago)
        is_post = False
        action = ""
        form = []

        if not isinstance(pedido, tuple):
            if 2 == medio_pago[0]:  #  WEBPAY
                try:
                    transaction = Webpay(
                        self.configuration_webpay
                    ).getNormalTransaction()
                    amount = pedido[
                        "total"
                    ]  # Identificador que será retornado en el callback de resultado:
                    sessionId = pedido[
                        "cookie_pedido"
                    ]  # Identificador único de orden de compra:
                    buyOrder = pedido["cookie_pedido"]
                    returnUrl = functions.generar_url(
                        [self.url[0], "process".medio_pago[0], pedido["cookie_pedido"]]
                    )
                    finalUrl = functions.generar_url(
                        [self.url[0], "pago".medio_pago[0], pedido["cookie_pedido"]]
                    )
                    initResult = transaction.initTransaction(
                        amount, buyOrder, sessionId, returnUrl, finalUrl
                    )

                    formAction = initResult.url
                    tokenWs = initResult.token
                    is_post = True
                    action = formAction
                    form.append({"field": "token_ws", "value": tokenWs})
                except Exception as e:
                    mensaje = "Hubo un error al inicial el proceso webpay. Por favor intenta más tarde."
                    config = app.get_config()
                    if config["debug"]:
                        mensaje += "<br/><br/><br/><br/>" + e

                    pedido = ("order/error", {"mensaje": mensaje})

        if not isinstance(pedido, tuple):
            seo_cuenta = seo_model.getById(9)
            data = {}
            data["title"] = medio_pago["titulo"]
            data["description"] = medio_pago["resumen"]
            data["is_post"] = is_post
            data["action"] = action
            data["form"] = form
            data["url_back"] = functions.generar_url(
                [seo_cuenta["url"], "pedido", pedido["cookie_pedido"]]
            )
            data["url_next"] = functions.generar_url(
                [self.url[0], "pago"+str(medio_pago[0]), pedido["cookie_pedido"]]
            )
            ret["body"].append(("payment/resumen", data))
        else:
            ret["body"].append(pedido)

        f = footer()
        ret["body"] += f.normal()["body"]
        return ret

    def pago1(self, var=[]):
        ret = {"body": []}
        self.meta(self.seo)
        self.url.append("pago1")
        idmedio = 1
        medio_pago = self.verificar_medio_pago(var[0], idmedio)

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
        ret["body"] += ba.individual(
            self.seo["banner"],
            "Pago via " + medio_pago["titulo"],
            self.metadata["title"],
        )["body"]


        f = footer()
        ret["body"] += f.normal()["body"]
        return ret

    def process2(self, var=[]):
        ret = {"body": []}
        error = True
        mensaje = ""
        campos = app.post
        if "token_ws" in campos:
            token = campos["token_ws"]

            transaction = Webpay(self.configuration_webpay).getNormalTransaction()
            result = transaction.getTransactionResult(token)
            output = result.detailOutput

            if 0 == output.responseCode:
                idmedio = 2
                cookie = output.buyOrder
                medio_pago = self.verificar_medio_pago(cookie, idmedio)
                pedido = self.verificar_pedido(medio_pago, False)
                if not isinstance(pedido, tuple):
                    self.update_pedido(
                        pedido, medio_pago, 4, result.transactionDate
                    )  # estado de pedido: pagado
                    seo_cuenta = seo_model.getById(9)
                    url_back = functions.generar_url(
                        array(seo_cuenta["url"], "pedido", pedido["cookie_pedido"])
                    )
                    campos = {}
                    campos["Estado del pedido"] = "Pagado"
                    campos["Medio de pago"] = medio_pago["titulo"]
                    campos["Código de pedido"] = pedido["cookie_pedido"]
                    campos["Total del pedido"] = functions.formato_precio(
                        pedido["total"]
                    )

                    respuesta = self.email(pedido, "", "", campos, url_back)
                    data = {}
                    data["action"] = result.urlRedirection
                    form = []
                    form.append({"field": "token_ws", "value": token})
                    data["form"] = form
                    ret["body"].append(("payment/post", data))
                    error = False
                else:
                    mensaje = "Este pedido no se puede procesar, ya está pagado o aún no se ha completado. Por favor intenta más tarde o selecciona otro medio de pago."

            else:
                result.sessionId
                result.transactionDate
                result.urlRedirection
                output.authorizationCode
                output.responseCode
                output.amount
                output.buyOrder
                mensaje = "Hubo un error al procesar tu pago, por favor intenta más tarde o selecciona otro medio de pago."

        if error:
            h = head(self.metadata)
            ret_head = h.normal()
            if ret_head["headers"] != "":
                return ret_head
            ret["body"] += ret_head["body"]

            he = header()
            ret["body"] += he.normal()["body"]

            ba = banner()
            ret["body"] += ba.individual(
                self.seo["banner"],
                "Pago via ".medio_pago["titulo"],
                self.metadata["title"],
            )["body"]

            pedido = ("order/error", {"mensaje": mensaje})

            f = footer()
            ret["body"] += f.normal()["body"]
        return ret

    def pago2(self, var=[]):
        ret = {"body": []}
        self.meta(self.seo)
        self.url.append("pago2")
        idmedio = 2
        medio_pago = self.verificar_medio_pago(var[0], idmedio)

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
        ret["body"] += ba.individual(
            self.seo["banner"],
            "Pago via " + medio_pago["titulo"],
            self.metadata["title"],
        )["body"]

        pedido = self.verificar_pedido(medio_pago, True, True)
        if not isinstance(pedido, tuple):
            seo_cuenta = seo_model.getById(9)
            url_back = functions.generar_url(
                [seo_cuenta["url"], "pedido", pedido["cookie_pedido"]]
            )
            data = {}
            data["title"] = medio_pago["titulo"]
            data["description"] = medio_pago["descripcion"]
            data["url_back"] = url_back
            ret["body"].append(("payment/confirmation", data))

        f = footer()
        ret["body"] += f.normal()["body"]
        return ret

    @staticmethod
    def email(pedido, titulo="", cabecera="", campos={}, url_pedido=""):
        nombre_sitio = app.title
        config = app.get_config()
        email_empresa = config["main_email"]
        body_email = {
            "template": "pedido",
            "titulo": "Pedido " + pedido["cookie_pedido"] + " Pago realizado",
            "cabecera": "Estimado {}, aquí enviamos su información de pago. Si tiene alguna duda, no dude en contactarse con el centro de atención al cliente de {}".format(
                pedido["nombre"], nombre_sitio
            ),
        }
        if "" != cabecera:
            body_email["cabecera"] = cabecera

        if "" != titulo:
            body_email["titulo"] = titulo

        body_email["campos_largos"] = {
            "": 'Puedes ver el detalle de tu pedido <a href="'
            + url_pedido
            + '"><b>haciendo click aquí</b></a>'
        }
        body_email["campos"] = campos
        imagenes = []
        adjuntos = []
        body = email.body_email(body_email)
        respuesta = email.enviar_email(
            [pedido["email"], email_empresa],
            body_email["titulo"],
            body,
            adjuntos,
            imagenes,
        )
        return respuesta

