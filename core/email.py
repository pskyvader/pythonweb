from .app import app
from .view import view


class email:
    @staticmethod
    def body_email(body_email):
        config = app.get_config();
        data = {}
        data['dominio'] = config['domain']
        data['email_empresa'] = config['main_email']
        data['email_from'] = config['email_from']
        data['nombre_sitio'] = config['title']
        data['color_primario'] = config['color_primario']
        data['color_secundario'] = config['color_secundario']
        data['logo'] = 'cid:logo'
        data['titulo'] = body_email['titulo']
        data['cabecera'] = body_email['cabecera']
        data['campos']=body_email['campos']
        data['campos_largos']=body_email['campos_largos']
        template = body_email['template']
        body=view.render([(template, data)],True,view.get_theme()+'mail/')
        return body