from core.view import view
from core.functions import functions

def init(var):
    h = home()
    if len(var) > 0:
        if hasattr(h, var[0]) and callable(getattr(h, var[0])):
            fun = var[0]
            del var[0]
            method=getattr(h, fun)
            ret = method(var)
        else:
            ret = {
                'error': 404,
            }
    else:
        ret = h.index()
    return ret




class home:
    url = ['home']
    metadata = {'title': 'Home', 'modulo': 'home'}

    def index(self):
        from core.app import app
        from .head import head
        ret = {}
        url_return=functions.url_redirect(self.url)
        if url_return!='':
            ret['error']=301
            ret['redirect']=url_return
            return ret
        
        h = head(self.metadata)
        ret_head=h.normal()
        if ret_head['header']!='':
            return ret_head
        
        view.add('title', 'index')
        view.add('var', str(app.post.getfirst("ajax")))
        breadcrumb=[
            {'active':'active','url':'aaaa','title':'titulo'},
            {'active':'','url':'bbb','title':'titulo2'},
            {'active':'active','url':'ccc','title':'titulo3'},
        ]
        view.add('breadcrumb', breadcrumb)
        ret['body'] = view.render('home')
        return ret

    def ver(self,var):
        ret = {}
        view.add('title', 'ver')
        ret['body'] = view.render('home')
        return ret
