
from core.email import email
from core.view import view


class previewmail():
    @classmethod
    def index(cls, var):
        body_email = {
            'body': view.get_theme() + 'mail/recuperar_password.html',
            'titulo': "Recuperación de contraseña",
            'cabecera': "Estimado " + admin["nombre"] + ", se ha solicitado la recuperación de contraseña en " + nombre_sitio,
                        'campos': {'Contraseña (sin espacios)': password},
                        'campos_largos': {},
        }
        body = email.body_email(body_email)
