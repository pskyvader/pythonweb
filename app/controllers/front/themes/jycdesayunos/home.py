from core.app import app
from core.file import file
from core.image import image
from core.functions import functions

from app.models.banner import banner as banner_model

from .base import base

from .head import head
from .header import header
from .banner import banner
from .breadcrumb import breadcrumb
from .footer import footer

class home(base):
    def __init__(self):
        super().__init__(app.get["idseo"])


     def index(self):
        ret = {"body": []}
        self.meta(self.seo)

        var = {}
        if self.seo["tipo_modulo"] != 0:
            var["tipo"] = self.seo["tipo_modulo"]

        if self.modulo["hijos"]:
            var["idpadre"] = 0

        row = seccion_model.getAll(var)

        if len(row) > 0:
            self.url = functions.url_seccion([self.url[0], "detail"], row[0], True)

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


        $row_banner = banner_model::getAll(array('tipo' => 1));

        ba = banner()
        ret["body"] += ba.individual(
            self.seo["banner"], self.metadata["title"], self.seo["subtitulo"]
        )["body"]
