

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
    
