from core.functions import functions
from core.view import view
from core.app import app
from core.image import image
from app.models.logo import logo as logo_model


class header:
    data = {'logo': '', 'url_exit': '', }

    def normal(self):
        ret = {'body': ''}
        if 'ajax' not in app.post:
            logo = logo_model.getById(3);
            self.data['logo_max'] = image.generar_url(logo['foto'][0], 'panel_max');
            logo = logo_model.getById(4);
            self.data['logo_min'] = image.generar_url(logo['foto'][0], 'panel_min');
            self.data['url_exit'] = functions.generar_url(['logout'], False)
            view.add_array(self.data)
            view.add('date', functions.current_time())
            ret['body'] = view.render('header')
        return ret
