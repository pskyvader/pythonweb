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

    def __init__(self):
        super().__init__(None)

    @classmethod
    def index(cls):
        ret = {'body':''}
        if not administrador_model.verificar_sesion():
            cls.url = ['login', 'index', 'home']
        
        url_return=functions.url_redirect(cls.url)
        if url_return!='':
            ret['error']=301
            ret['redirect']=url_return
            return ret
        
        registros=administrador_model.getAll(where={'idpadre':1},condiciones={'limit':1,'limit2':0})
        h = head(cls.metadata)
        ret_head=h.normal()
        if ret_head['headers']!='':
            return ret_head
        ret['body']+=ret_head['body']
        
        he=header()
        #ret_header=he.normal()
        #ret['body']+=ret_header['body']
        ret['body']+=he.normal()['body']

        asi = aside()
        ret_asi=asi.normal()
        ret['body']+=ret_asi['body']


        view.add('title', 'index')
        view.add('var', str(registros))
        breadcrumb=[
            {'active':'active','url':'aaaa','title':'titulo'},
            {'active':'','url':'bbb','title':'titulo2'},
            {'active':'active','url':'ccc','title':'titulo3'},
        ]
        view.add('breadcrumb', breadcrumb)
        ret['body'] += view.render('home')


        f = footer()
        ret_f=f.normal()
        ret['body']+=ret_f['body']

        return ret