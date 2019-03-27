from .app import app

class email:
    @staticmethod
    def body_email(body_email):
        config = app::getConfig()
        dominio = config['domain']
        email_empresa = config['main_email']
        from = config['email_from']
        nombre_sitio = config['title']
        color_primario = config['color_primario']
        color_secundario = config['color_secundario']
        logo='cid:logo'

        body = file_get_contents(body_email['body'])

        body = str_replace('{logo}', logo, body)
        body = str_replace('{email_empresa}', email_empresa, body)
        body = str_replace('{dominio}', dominio, body)
        body = str_replace('{color_primario}', color_primario, body)
        body = str_replace('{color_secundario}', color_secundario, body)
        body = str_replace('{nombre_sitio}', nombre_sitio, body)
        body = str_replace('{titulo}', body_email['titulo'], body)
        body = str_replace('{cabecera}', body_email['cabecera'], body)

        c1 = ""
        if (isset(body_email['campos']) && count(body_email['campos']) > 0) {
            campos = body_email['campos']
            c = file_get_contents(view::get_theme() . 'mail/campos.html')
            c = str_replace('{color_primario}', color_primario, c)
            c = str_replace('{color_secundario}', color_secundario, c)
            foreach (campos as key => value) {
                c1 .= str_replace('{value}', value, str_replace('{key}', key, c))
            }
        }
        body = str_replace('{campos}', c1, body)

        c1 = ""
        if (isset(body_email['campos_largos']) && count(body_email['campos_largos']) > 0) {
            campos_largos = body_email['campos_largos']
            c = file_get_contents(view::get_theme() . 'mail/campos_largos.html')
            c = str_replace('{color_primario}', color_primario, c)
            c = str_replace('{color_secundario}', color_secundario, c)
            foreach (campos_largos as key => value) {
                c1 .= str_replace('{value}', value, str_replace('{key}', key, c))
            }
        }
        body = str_replace('{campos_largos}', c1, body)
        return body
    }