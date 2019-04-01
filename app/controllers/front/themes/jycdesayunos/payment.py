

from app.models.mediopago import mediopago as mediopago_model
from app.models.seo import seo as seo_model

from core.app import app
from core.functions import functions


class payment(base):
    cookie               = ''
    configuration_webpay = None
    def __init__(self):
        super().__init__(app.idseo, False)
        #self.configuration_webpay = Configuration.forTestingWebpayPlusNormal()
    
    def index():
        seo_home = seo_model.getById(1)
        url_return = functions.url_redirect(seo_home['url'])
        if url_return != "":
            ret["error"] = 301
            ret["redirect"] = url_return
            return ret
    
    def verificar_medio_pago(cookie:str = '', idmedio:int):
    
        """ comprueba si existe el medio de pago, sino vuelve al home
        :param cookie:str:
        :param idmedio:int:
    
        :raises:
    
        :rtype: mixed
        """    
        medio_pago = None
        if '' != cookie:
            mp = mediopago_model.getById(idmedio)
            if isset(mp['estado']):
                cookie       = functions.test_input(cookie)
                this->cookie = cookie
                this->url[]  = cookie
                medio_pago   = mp
            } else {
                seo_home  = seo_model.getById(1)
                this->url = array(seo_home['url'])
            }
        } else {
            seo_home  = seo_model.getById(1)
            this->url = array(seo_home['url'])
        }
        return medio_pago
    }
