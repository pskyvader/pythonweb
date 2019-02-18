from core.app import app
from core.functions import functions
import json


def init(var):
    h = manifest()
    ret = h.index()
    return ret


class manifest:
    def index(self):
        ret = {'headers': [ ('Content-Type', 'application/json; charset=utf-8') ], 'body': ''}
        version_application = 1
        config = app.get_config()
        #logo = logo_model.getById(7)
        logo = {'foto': ['aaa']}
        manifest = {
            'short_name': config['short_title'],
            'name': config['title'],
            'icons': [
                {
                    'src': image.generar_url(logo['foto'][0], 'icono50'),
                    'type': 'image/png',
                    'sizes': '50x50'
                }, {
                    'src': image.generar_url(logo['foto'][0], 'icono100'),
                    'type': 'image/png',
                    'sizes': '100x100'
                }, {
                    'src': image.generar_url(logo['foto'][0], 'icono200'),
                    'type': 'image/png',
                    'sizes': '200x200'
                }, {
                    'src': image.generar_url(logo['foto'][0], 'icono600'),
                    'type': 'image/png',
                    'sizes': '600x600'
                }
            ],
            "start_url": functions.generar_url(["application", "index", version_application], False),
            "background_color": config['color_secundario'],
            "display": "standalone",
            "theme_color": config['color_primario'],
        }
        ret['body'] = json.dumps(manifest)
        return ret
