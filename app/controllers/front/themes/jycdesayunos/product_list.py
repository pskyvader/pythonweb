from .base import base


from app.models.configuracion import configuracion as configuracion_model
from app.models.productocategoria import productocategoria as productocategoria_model

from core.app import app
from core.functions import functions


class product_list(base):
    view = "grid"
    order = "orden"
    search = ""
    page = 1
    limit = 6
    count = 0

    def __init__(self):
        super().__init__(app.idseo)

        self.view = (
            "list" if "view" in app.get and app.get["view"] == "list" else "grid"
        )
        self.order = (
            functions.remove_tags(app.get["order"]).strip()
            if "order" in app.get and app.get["order"] != ""
            else "orden"
        )
        self.search = (
            functions.remove_tags(app.get["search"]).strip()
            if "search" in app.get
            else ""
        )
        self.page = (
            int(functions.remove_tags(app.get["page"]).strip())
            if "page" in app.get and app.get["page"] != ""
            else 1
        )
        self.limit = (
            int(functions.remove_tags(app.get["limit"]).strip())
            if "limit" in app.get and app.get["limit"] != ""
            else 6
        )



















    def is_search(self):
        return {'search':self.search}
        
    def sidebar(self,categoria = None):
        variables = {}
        if self.seo['tipo_modulo'] != 0:
            variables['tipo'] = self.seo['tipo_modulo']
        
        if self.modulo['hijos']:
            if categoria == None:
                variables['idpadre'] = 0
            else:
                variables['idpadre'] = categoria[0]
            
        
        row                = productocategoria_model.getAll(variables)
        sidebar_categories = []
        for s in row:
            sidebar_categories.append({'title' : s['titulo'], 'active' : '', 'url' : functions.url_seccion([self.url[0], 'category'], s, False, None)})
        

        is_sidebar_categories = (len(sidebar_categories) > 0)
        is_sidebar_prices     = False
        if is_sidebar_categories or is_sidebar_prices:
            is_sidebar = True
        else:
            is_sidebar = False
        

        if is_sidebar:
            data={}
            data['title']= "Categorias"
            data['is_sidebar_category']= is_sidebar_categories
            data['sidebar_categories']= sidebar_categories
            data['is_sidebar_prices']= is_sidebar_prices
            return ('product/sidebar',data)
        else:
            return ""

    def orden_producto():
        orden_producto = configuracion_model.getByVariable('orden_producto')
        if not isinstance(orden_producto,bool):
            orden_producto = orden_producto.split(',')
            for op in orden_producto:
                op = op.split(':')
                for o in op:
                    o = trim(o)
                
        if not isinstance(orden_producto,list) or len(orden_producto) == 0:
            orden_producto = [
                ['orden', 'Recomendados'],
                ['ventas', 'Más vendidos'],
                ['precio ASC', 'Precio de menor a mayor'],
                ['precio DESC', 'Precio de mayor a menor'],
                ['titulo ASC', 'A-Z'],
                ['titulo DESC', 'Z-A'],
            ]
            orden_producto_guardar = {}

            for op in orden_producto:
                orden_producto_guardar.append(':'.join(op))
            
            orden_producto_guardar = ','.join(orden_producto_guardar)
            configuracion_model.setByVariable('orden_producto', orden_producto_guardar)

        orden_producto_mostrar = []
        for op in orden_producto:
            orden_producto_mostrar.append({
                'title'  : op[1],
                'action' : op[0],
                'active' : 'order' in app.get and app.get['order'] == op[0],
            })
        
        return {'view':self.view,'orden_producto': orden_producto_mostrar}
        

    def limit_producto(self):
        limits = {
            6   : {'action' : 6, 'title' : 6, 'active' : False},
            12  : {'action' : 12, 'title' : 12, 'active' : False},
            30  : {'action' : 30, 'title' : 30, 'active' : False},
            120 : {'action' : 120, 'title' : 120, 'active' : False},
        }

        if self.limit in limits:
            limits[self.limit]['active'] = True
        return ('limit_producto',limits)
    
    def product_list(categoria = None):
        where = array()
        if self.seo['tipo_modulo'] != 0:
            where['tipo'] = self.seo['tipo_modulo']
        }
        if categoria != None:
            where[productocategoria_model.idname] = categoria[0]
        }
        condiciones = array('order' : self.order)
        if self.search != '':
            condiciones['palabra'] = self.search
        }
        self.count = producto_model.getAll(where, condiciones, 'total')

        condiciones['limit'] = self.limit
        if self.page > 1:
            condiciones['limit']  = ((self.page - 1) * self.limit)
            condiciones['limit2'] = (self.limit)
        }

        productos = producto_model.getAll(where, condiciones)
        if len(productos) > 0:
            lista_productos = self.lista_productos(productos, 'detail', 'foto2')
            view.set('lista_productos', lista_productos)
            if self.view == 'grid':
                // Comprobar si existe o no sidebar, para agrandar o achicar el tamaño del producto
                variables = array()
                if self.seo['tipo_modulo'] != 0:
                    variables['tipo'] = self.seo['tipo_modulo']
                }
                if self.modulo['hijos']:
                    if categoria == None:
                        variables['idpadre'] = 0
                    else:
                        variables['idpadre'] = categoria[0]
                    }
                }
                count = productocategoria_model.getAll(variables, array(), 'total')
                if count > 0:
                    view.set('col-lg', 'col-lg-6')
                else:
                    view.set('col-lg', 'col-lg-4')
                }

                view.set('col-md', 'col-md-12')
                product_list = view.render('product/grid', False, True)
            else:
                product_list = view.render('product/list', False, True)
            }
        }
        return product_list
    }

    def pagination():
        pagination = array()
        rango      = 5
        min        = 1
        max        = (int) (self.count / self.limit)
        if max < (self.count / self.limit):
            max++
        }
        total = max
        sw    = False
        page  = self.page
        while (((max - min) + 1) > rango:
            if sw:
                if min != page and min + 1 != page:
                    min++
                }
            else:
                if max != page and max - 1 != page:
                    max--
                }
            }
            sw = !sw
        }

        aux_page = (isset(_GET['page'])) ? _GET['page'] : ''

        _GET['page'] = page - 1
        pagination[] = array(
            'class_page' : 'previous ' . ((page > 1) ? '' : 'disabled'),
            'url_page'   : ((page > 1) ? functions.generar_url(self.url) : functions.generar_url(self.url, False)),
            'text_page'  : '<i class="fa fa-angle-left"> </i>',
        )

        for (i = min i <= max i++:
            _GET['page'] = i
            pagination[] = array(
                'class_page' : ((page == i) ? 'active' : ''),
                'url_page'   : functions.generar_url(self.url),
                'text_page'  : i,
            )
        }

        _GET['page'] = page + 1
        pagination[] = array(
            'class_page' : 'next ' . ((page < total) ? '' : 'disabled'),
            'url_page'   : ((page < total) ? functions.generar_url(self.url) : functions.generar_url(self.url, False)),
            'text_page'  : '<i class="fa fa-angle-right"> </i> ',
        )

        if aux_page != '':
            _GET['page'] = aux_page
        else:
            unset(_GET['page'])
        }
        view.set('pagination', pagination)
    }

    def lista_productos(row, url = 'detail', recorte = 'foto1'):
        lista = array()
        foreach (row as key : v:
            portada = image.portada(v['foto'])
            c       = array(
                'id'           : v[0],
                'title'        : v['titulo'],
                'is_descuento' : (v['precio_final'] != v['precio']),
                'price'        : functions.formato_precio(v['precio_final']),
                'old_price'    : functions.formato_precio(v['precio']),
                'is_stock'     : (v['stock'] > 0),
                'image'        : image.generar_url(portada, recorte),
                'description'  : strip_tags(v['resumen']),
                'srcset'       : array(),
                'url'          : functions.url_seccion(array(self.url[0], url), v),
            )
            src = image.generar_url(portada, recorte, 'webp')
            if src != '':
                c['srcset'][] = array('media' : '', 'src' : src, 'type' : 'image/webp')
            }
            if c['image'] != "":
                lista[] = c
            }
        }
        return lista
    }
