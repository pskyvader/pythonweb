from .base import base
from app.models.administrador import administrador as administrador_model


from app.models.logo import logo as logo_model

from .head import head
from .footer import footer

from core.app import app
from core.functions import functions
from core.image import image
from core.view import view

class application(base):
    url = ['application']
    metadata = {'title' : 'application','modulo':'application'}
    breadcrumb = []

    @classmethod
    def index(cls):
        '''Controlador de lista_class de elementos base, puede ser sobreescrito en el controlador de cada modulo'''
        ret = {'body': ''}
        # Clase para enviar a controlador de lista_class
        url_final=cls.url.copy()
        if not administrador_model.verificar_sesion():
            url_final = ['login', 'index'] + url_final
        # verificar sesion o redireccionar a login
        url_return = functions.url_redirect(url_final)
        if url_return != '':
            ret['error'] = 301
            ret['redirect'] = url_return
            return ret



        h = head(cls.metadata)
        ret_head=h.normal()
        if ret_head['headers']!='':
            return ret_head
        ret['body']+=ret_head['body']
        

        config = app.get_config()
        logo = logo_model.getById(7)
        view.add('color_primario', config['color_primario'])
        view.add('color_secundario', config['color_secundario'])
        view.add('logo', image.generar_url(logo['foto'][0], 'icono600'))
        view.add('path', functions.generar_url(url_final))
        view.render('application')

        ret['body'] += view.render('home')


        f = footer()
        ret['body']+=f.normal()['body']



        return ret