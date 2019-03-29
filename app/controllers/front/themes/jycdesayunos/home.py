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
    @classmethod
    def index(cls):
        ret = {"body": []}
        cls.meta(cls.seo)

        var = {}
        if cls.seo["tipo_modulo"] != 0:
            var["tipo"] = cls.seo["tipo_modulo"]

        if cls.modulo["hijos"]:
            var["idpadre"] = 0

        row = seccion_model.getAll(var)

        if len(row) > 0:
            cls.url = functions.url_seccion([cls.url[0], "detail"], row[0], True)

        url_return = functions.url_redirect(cls.url)
        if url_return != "":
            ret["error"] = 301
            ret["redirect"] = url_return
            return ret

        h = head(cls.metadata)
        ret_head = h.normal()
        if ret_head["headers"] != "":
            return ret_head
        ret["body"] += ret_head["body"]

        he = header()
        ret["body"] += he.normal()["body"]

        row_banner = banner_model.getAll({'tipo' :1})
        ba = banner()
        ret["body"] += ba.normal(row_banner)["body"]

        #bc = breadcrumb()
        #ret["body"] += bc.normal(cls.breadcrumb)["body"]


        secciones_destacadas = seccion_model.getAll({'tipo' : 3, 'destacado' : True})
        seo                  = seo.getById(7)
        for seccion in secciones_destacadas:
            data={}
            data['title']= seccion['titulo']
            data['subtitle']= seccion['subtitulo']
            data['text']= seccion['resumen']
            data['url']= functions.url_seccion([seo['url'], 'detail'], seccion)
            data['image']= image.generar_url(image.portada(seccion['foto']), '')
            ret["body"].append(("home-text", data.copy()))
            
        productos_destacados = producto_model.getAll({'tipo' : 1, 'destacado' : True},{'limit':6})
        if len(productos_destacados)>0:
            data={}
            #seo_productos          = seo.getById(8)
            #this->url[0] = seo_productos['url']
            app.get['idseo']=8
            pl              = product_list.product_list() #product_list.py
            lista_productos = pl.lista_productos(productos_destacados, 'detail', 'foto2') #Lista de productos, renderiza vista
            data['lista_productos']= lista_productos
            data['col-md']= 'col-md-6'
            data['col-lg']= 'col-lg-4'
            product_list = ('product/grid',data.copy())
            data={}
            data['product_list']= product_list
            #view.set('title',seo_productos['titulo'])
            data['title']= "Nuestros productos destacados"
            ret["body"].append(("home-products", data.copy()))
            
        
        f = footer()
        ret["body"] += f.normal()["body"]
        return ret