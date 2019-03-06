from core.app import app
from core.view import view
from core.functions import functions
from .base import base
from .head import head
from .header import header
from .aside import aside
from .footer import footer
from app.models.administrador import administrador as administrador_model


class home(base):
    url = ['home']
    metadata = {'title': 'Home', 'modulo': 'home'}

    @classmethod
    def index(cls):
        ret = {'body':''}
        url_final=cls.url
        if not administrador_model.verificar_sesion():
            url_final = ['login', 'index', 'home']
        
        url_return=functions.url_redirect(url_final)
        if url_return!='':
            ret['error']=301
            ret['redirect']=url_return
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

        return ret