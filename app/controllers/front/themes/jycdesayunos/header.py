from core.functions import functions
from core.app import app
from core.image import image
from app.models.logo import logo as logo_model
from app.models.seo import seo as seo_model


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
            self.data['path']       = functions.generar_url(array(seo['url']),false)
            self.data['title']      = config['title']

            telefono = texto.getById(1)
            view.set('telefono', telefono['texto'])
            email = texto.getById(2)
            view.set('email', email['texto'])
            seo = seo.getById(8)
            view.set('product_url', functions.generar_url(array(seo['url']),false))
            view.set('search', isset(_GET['search'])?strip_tags(_GET['search']):"")

            view.render('header')


            logo = logo_model.getById(3)
            self.data['logo_max'] = image.generar_url(
                logo['foto'][0], 'panel_max')
            logo = logo_model.getById(4)
            self.data['logo_min'] = image.generar_url(
                logo['foto'][0], 'panel_min')
            self.data['url_exit'] = functions.generar_url(['logout'], False)
            self.data['date'] = functions.current_time()
            ret['body'].append(('header', self.data))
        return ret
