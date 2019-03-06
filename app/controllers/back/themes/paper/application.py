from .base import base
from app.models.administrador import administrador as administrador_model

from .head import head
from .header import header
from .aside import aside
from .footer import footer

from core.functions import functions

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
        
        he=header()
        ret['body']+=he.normal()['body']

        asi = aside()
        ret['body']+=asi.normal()['body']


        view.add('title', 'Home')
        breadcrumb=[
            {'url':functions.generar_url(url_final),'title':cls.metadata['title'],'active':'active'}
        ]
        view.add('breadcrumb', breadcrumb)
        ret['body'] += view.render('home')


        f = footer()
        ret['body']+=f.normal()['body']

        $head = new head($this->metadata);
        $head->normal();
        $config = app::getConfig();
        $logo = logo_model::getById(7);
        view::set('color_primario', $config['color_primario']);
        view::set('color_secundario', $config['color_secundario']);
        view::set('logo', image::generar_url($logo['foto'][0], 'icono600'));
        view::set('path', functions::generar_url($this->url));
        view::render('application');
        $footer = new footer();
        $footer->normal();

        return ret