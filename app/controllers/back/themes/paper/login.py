from core.functions import functions
from core.app import app
from app.models.administrador import administrador as administrador_model

def init(var):
    h = login()
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


class login:
    url = ['login','index']
    metadata = {'title': 'login', 'modulo': 'login'}

    def index(self,url):
        from datetime import datetime
        ret = {'body':''}
        self.url=self.url+url

        cookie_admin=functions.get_cookie('cookieadmin'+app.prefix_site)
        if cookie_admin!=False:
            logueado = administrador_model.login_cookie(cookie_admin)
            if logueado:
                if not url: 
                    self.url = ['home']
                else:
                    self.url = url
                    

        if 'bloqueo_administrador' in app.session and app.session['bloqueo_administrador']>datetime.now():
            exit("IP Bloqueada por intentos fallidos. Intente más tarde. tiempo: ".(intval(time())-intval(_SESSION['bloqueo_administrador']))." segundos")
        }
        
        if(isset(_SESSION['intento_administrador']) && _SESSION['intento_administrador']%5==0){
            _SESSION['bloqueo_administrador']=time()+60*(intval(_SESSION['intento_administrador'])/5)
            if(_SESSION['intento_administrador']>=15) bloquear_ip(getRealIP())
            _SESSION['intento_administrador']++
        }

        error_login=false
        if(isset(_POST['email']) && isset(_POST['pass']) && isset(_POST['token'])){
            if(_SESSION['login_token']['token']==_POST['token']){
                if(time()-_SESSION['login_token']['time']<=120){
                    if(!isset(_POST['recordar'])) _POST['recordar']=''
                    logueado=administrador_model::login(_POST['email'],_POST['pass'],_POST['recordar'])
                    if(logueado:
                        if(isset(_SESSION['intento_administrador'])) _SESSION['intento_administrador']=0
                        if(empty(url)) this->url = array('home')
                        else this->url=url
                    }else {
                        error_login=true
                        if(!isset(_SESSION['intento_administrador'])) _SESSION['intento_administrador']=0
                        _SESSION['intento_administrador']++
                    }
                }else{
                    error_login=true
                }
            }else{
                error_login=true
                if(!isset(_SESSION['intento_administrador'])) _SESSION['intento_administrador']=0
                _SESSION['intento_administrador']+=5
            }
        }

        url_return=functions.url_redirect(self.url)
        if url_return!='':
            ret['error']=301
            ret['redirect']=url_return
            return ret
        
        h = head(self.metadata)
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
        ret['body'] += view.render('login')


        f = footer()
        ret_f=f.normal()
        ret['body']+=ret_f['body']

        return ret