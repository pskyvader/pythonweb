from core.functions import functions
from core.app import app
from core.image import image

from app.models.logo import logo as logo_model
from app.models.moduloconfiguracion import moduloconfiguracion as moduloconfiguracion_model
from app.models.seo import seo as seo_model
from app.models.texto import texto as texto_model



class header:
    data = {'logo': ''}

    def normal(self):
        ret = {'body': []}
        if 'ajax' not in app.post:
            self.data['header-top'] = self.header_top()
            self.data['cart']       = self.header_cart()
            self.data['menu']       = self.menu()
            config             = app.get_config()
            logo               = logo_model.getById(5)
            portada=image.portada(logo['foto'])
            self.data['logo']       = image.generar_url(portada, 'sitio')
            seo                = seo_model.getById(1)
            self.data['path']       = functions.generar_url([seo['url']],False)
            self.data['title']      = config['title']

            telefono = texto_model.getById(1)
            self.data['telefono']= telefono['texto']
            email = texto_model.getById(2)
            self.data['email']= email['texto']
            seo = seo_model.getById(8)
            self.data['product_url']= functions.generar_url([seo['url']],False)
            self.data['search']= functions.remove_tags(app.get['search']) if 'search' in app.get else ""
            ret['body'].append(('header', self.data))
        return ret

    def header_top(self):
        redes_sociales = []
        rss            = texto_model.getAll({'tipo' : 2})
        for r in rss:
            redes_sociales.append(
                    {
                        "url": functions.ruta(r["url"]),
                        "icon": r["texto"],
                        "title": r["titulo"],
                    }
                )
        data={}
        data['social']= redes_sociales
        return ('header-top',data)
    
    def header_cart(self):
        return ('header-top',{})
    
    def menu(self):
        lista_menu = []
        seo        = seo_model.getAll()
        for s in seo:
            if s['submenu'] and s['modulo_back'] != '' and s['modulo_back'] != 'none':
                if s['menu']:
                    url = functions.generar_url([s['url']], False)
                else:
                    url = ''
                
                menu                = {'titulo' : s['titulo'], 'link' : url, 'active' : s['url']}
                moduloconfiguracion = moduloconfiguracion_model.getByModulo(s['modulo_back'])
                if isset(moduloconfiguracion[0]):
                    modulo = modulo_model.getAll(array('idmoduloconfiguracion' : moduloconfiguracion[0], 'tipo' : s['tipo_modulo']), array('limit' : 1))
                    if isset(modulo[0]):
                        c     = '\app\models\\' . s['modulo_back']
                        class = new c
                        var   = array()
                        if s['tipo_modulo'] != 0:
                            var['tipo'] = s['tipo_modulo']
                        }
                        if isset(modulo[0]['hijos']) and modulo[0]['hijos']:
                            var['idpadre'] = 0
                        }
                        row   = class.getAll(var)
                        hijos = array()
                        foreach (row as key : sub:
                            sub_url = "detail"
                            if isset(s['link_menu']) and s['link_menu'] != '':
                                sub_url = s['link_menu']
                            }

                            hijos[] = array('titulo' : sub['titulo'], 'link' : functions.url_seccion(array(s['url'], sub_url), sub), 'active' : sub['url'])
                        }
                        menu['hijo'] = hijos
                    }
                }

                lista_menu[] = menu
            else:
                if s['menu']:
                    lista_menu[] = array('titulo' : s['titulo'], 'link' : functions.generar_url(array(s['url']), False), 'active' : s['url'])
                }
            }
        }

        menu = this->generar_menu(lista_menu)

        return menu
    }