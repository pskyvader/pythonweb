from core.functions import functions
from core.app import app
from core.view import view
from app.models.administrador import administrador as administrador_model
from .head import head
from .footer import footer


def init(var):
    h = login()
    if len(var) > 0:
        if hasattr(h, var[0]) and callable(getattr(h, var[0])):
            fun = var[0]
            del var[0]
            method = getattr(h, fun)
            ret = method(var)
        else:
            ret = {
                'error': 404,
            }
    else:
        ret = h.index({})
    return ret


class login:
    url = ['login', 'index']
    metadata = {'title': 'login', 'modulo': 'login'}

    def index(self, url):
        from time import time
        ret = {'body': ''}
        self.url = self.url+url

        cookie_admin = functions.get_cookie('cookieadmin'+app.prefix_site)
        if cookie_admin != False:
            logueado = administrador_model.login_cookie(cookie_admin)
            if logueado:
                if not url:
                    self.url = ['home']
                else:
                    self.url = url

        if 'bloqueo_administrador' in app.session and app.session['bloqueo_administrador'] > time():
            ret['body'] = "IP Bloqueada por intentos fallidos. Intente más tarde. tiempo: " + \
                time()-app.session['bloqueo_administrador']+" segundos"
            return ret

        if 'intento_administrador' in app.session and int(app.session['intento_administrador']) % 5 == 0:
            app.session['bloqueo_administrador'] = time() + 60*int(app.session['intento_administrador'])
            # if app.session['intento_administrador']>=15) bloquear_ip(getRealIP())
            app.session['intento_administrador'] +=1

        error_login = False
        if 'email' in app.post and 'pass' in app.post and 'token' in app.post:
            print(app.session['login_token'])
            if 'login_token' in app.session and app.session['login_token']['token'] == app.post['token']:
                if time()-int(app.session['login_token']['time']) <= 120:
                    if not 'recordar' in app.post:
                        app.post['recordar'] = ''
                    logueado = administrador_model.login(
                        app.post['email'], app.post['pass'], app.post['recordar'])
                    if logueado:
                        if 'intento_administrador' in app.session:
                            app.session['intento_administrador'] = 0
                        if not url:
                            self.url = ['home']
                        else:
                            self.url = url
                    else:
                        error_login = True
                        if not 'intento_administrador' in app.session:
                            app.session['intento_administrador'] = 1
                        app.session['intento_administrador'] += 1
                else:
                    error_login = True
            else:
                error_login = True
                if not 'intento_administrador' in app.session:
                    app.session['intento_administrador'] = 0
                app.session['intento_administrador'] += 5

        url_return = functions.url_redirect(self.url)
        if url_return != '':
            ret['error'] = 301
            ret['redirect'] = url_return
            return ret

        token = functions.generar_pass(20)
        app.session['login_token'] = {'token': token, 'time': time()}
        h = head(self.metadata)
        ret_head = h.normal()
        if ret_head['headers'] != '':
            return ret_head
        ret['body'] += ret_head['body']

        view.add('logo', '')
        view.add('error_login', error_login)
        view.add('token', token)
        view.add('url_recuperar', functions.generar_url(["recuperar"]))
        # logo=logo_model.getById(2)
        #view.add('logo', image.generar_url(logo['foto'][0], 'login'))
        ret['body'] += view.render('login')

        f = footer()
        ret_f = f.normal()
        ret['body'] += ret_f['body']

        return ret
