

from app.models.productocategoria import productocategoria as productocategoria_model

from .base import base
from .product_list import product_list


from .head import head
from .header import header
from .banner import banner
from .breadcrumb import breadcrumb
from .footer import footer

from core.app import app
from core.functions import functions

class product(base):
    def __init__(self):
        super().__init__(app.idseo)







    def index(self):
        ret = {"body": []}
        self.meta(self.seo)
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




        pl           = product_list() #product_list.php
        product_list = pl.product_list() #Lista de productos, renderiza vista
        sidebar      = pl.sidebar() # genera sidebar, renderiza vista
        pl.orden_producto() # genera lista de filtros
        pl.limit_producto() #genera lista de cantidad de productos por pagina
        pl.pagination() # genera paginador
        pl.is_search() # Genera texto de busqueda, si existe

        data={}
        data['product_list']= product_list
        data['sidebar']= sidebar
        
        ret["body"].append(("product/category", data))

        f = footer()
        ret["body"] += f.normal()["body"]
        return ret
    

    def category(self,var = []):
        ret = {"body": []}
        if len(var)>0:
            id        = functions.get_idseccion(var[0])
            categoria = productocategoria_model.getById(id)
            if len(categoria)>0:
                self.url          = functions.url_seccion([self.url[0], 'category'], categoria, True)
                self.breadcrumb.append({'url' : functions.generar_url(self.url), 'title' : categoria['titulo']})
            
        
        url_return = functions.url_redirect(self.url)
        if url_return != "":
            ret["error"] = 301
            ret["redirect"] = url_return
            return ret
        self.meta(categoria)


        h = head(self.metadata)
        ret_head = h.normal()
        if ret_head["headers"] != "":
            return ret_head
        ret["body"] += ret_head["body"]

        he = header()
        ret["body"] += he.normal()["body"]

        ba = banner()
        ret["body"] += ba.individual(self.seo["banner"], self.seo["titulo"],self.metadata['title'])["body"]

        bc = breadcrumb()
        ret["body"] += bc.normal(self.breadcrumb)["body"]


        pl           = product_list() #product_list.php
        product_list = pl.product_list(categoria) #Lista de productos, renderiza vista
        sidebar      = pl.sidebar(categoria) # genera sidebar, renderiza vista
        pl.orden_producto() # genera lista de filtros
        pl.limit_producto() #genera lista de cantidad de productos por pagina
        pl.pagination() # genera paginador
        pl.is_search() # Genera texto de busqueda, si existe


        data={}
        data['product_list']= product_list
        data['sidebar']= sidebar
        
        ret["body"].append(("product/category", data))

        f = footer()
        ret["body"] += f.normal()["body"]
        return ret
        

    public function detail(var = array())
    {
        if (isset(var[0])) {
            id       = functions.get_idseccion(var[0])
            producto = producto_model.getById(id)
            if (isset(producto[0])) {
                self.url          = functions.url_seccion(array(self.url[0], 'detail'), producto, True)
                self.breadcrumb[] = array('url' : functions.generar_url(self.url), 'title' : producto['titulo'])
            }
        }
        functions.url_redirect(self.url)
        self.meta(producto)

        head = new head(self.metadata)
        head.normal()

        header = new header()
        header.normal()

        banner = new banner()
        banner.individual(self.seo['banner'], producto['titulo'])

        #breadcrumb = new breadcrumb()
        #breadcrumb.normal(self.breadcrumb)
        pl      = new product_list() #product_list.php
        sidebar = pl.sidebar() # genera sidebar, renderiza vista
        pd      = new product_detail(producto, self.url)
        tabs    = pd.tabs()
        pd.galeria()
        pd.resumen()

        view.set('sidebar', sidebar)
        view.set('tabs', tabs)
        view.set('url', functions.generar_url(self.url))
        if(self.metadata['image']!=''){
            view.set('imagen_portada', self.metadata['image'])
        }else{
            view.set('imagen_portada', self.metadata['logo'])
        }

        view.render('product/detail')

        footer = new footer()
        footer.normal()
    }