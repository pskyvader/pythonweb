from core.functions import functions
from core.app import app
from core.image import image
from app.models.logo import logo as logo_model
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

            telefono = texto.getById(1)
            self.data['telefono']= telefono['texto']
            email = texto.getById(2)
            self.data['email']= email['texto']
            seo = seo.getById(8)
            self.data['product_url']= functions.generar_url([seo['url']],False)
            self.data['search']= functions.remove_tags(app.get['search']) if 'search' in app.get else ""
            ret['body'].append(('header', self.data))
        return ret

    def header_top(self):
        redes_sociales = array()
        rss            = texto_model.getAll(array('tipo' => 2))
        foreach (rss as key => r) {
            redes_sociales[] = array('url' => functions.ruta(r['url']), 'icon' => r['texto'], 'title' => r['titulo'])
        }

        view.set('social', redes_sociales)
        view.set('is_social', (count(redes_sociales) > 0))
        view.set('is_social', false)
        return view.render('header-top', false, true)
    }
