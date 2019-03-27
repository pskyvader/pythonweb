
from core.email import email
from core.view import view


class previewmail():
    @classmethod
    def init(cls, var={}):
        ret = {'body': ''}
        nombre = 'pablo'
        nombre_sitio = 'sitio python'
        password = '123456789'
        body_email = {
            'template': 'recuperar_password',
            'titulo': "Recuperación de contraseña",
            'cabecera': "Estimado " + nombre + ", se ha solicitado la recuperación de contraseña en " + nombre_sitio,
            'campos': {'Contraseña (sin espacios)': password},
            'campos_largos': {},
        }
        body = email.body_email(body_email)
        ret['body']=body
        return ret

