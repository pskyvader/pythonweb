from core.app import app
from core.functions import functions
from core.view import view
import json


class head:
    data = {
        'favicon': '',
        'keywords': '',
        'description': '',
        'title': '',
        'current_url': '',
        'image': '',
        'color_primario': '',
        'manifest_url': '',
        'path': '',
        'modulo': '',
        'max_size': -1,
    }

    def __init__(self, metadata):
        for key, value in metadata.items():
            if key in self.data:
                head.data[key] = value

        config = app.get_config()
        head.data['current_url'] = functions.current_url()
        head.data['path'] = app.path
        head.data['color_primario'] = config['color_primario']
        head.data['googlemaps_key'] = config['googlemaps_key']
        # size=functions::get_max_size()
        #head.data['max_size'] = size
        # head.data['max_size_format'] = (size<0)?"Ilimitado":functions::file_size(size,true)

        titulo = head.data['title'] + ' - ' + config['title']
        if (len(titulo) > 75):
            titulo = head.data['title'] + ' - ' + config['short_title']

        if (len(titulo) > 75):
            titulo = head.data['title']

        if (len(titulo) > 75):
            titulo = head.data['title'][0:75]

        head.data['title'] = titulo

        # if (isset(metadata['image'])) {
        #   head.data['image'] = metadata['image']
        # }else{
        # logo = logo_model::getById(3)
        # head.data['image']=image::generar_url(logo['foto'][0], 'panel_max')
        # }
        # logo = logo_model::getById(1)
        # head.data['favicon'] = image::generar_url(logo['foto'][0], 'favicon')

        head.data['manifest_url'] = app.get_url() + 'manifest.js'

    def normal(self):
        ret = {'headers': '', 'body': ''}
        if app.post.getfirst("ajax") is None:
            if app.post.getfirst("ajax_header") is None:
                head.data['css'] = view.css()
                view.add_array(head.data)
                ret['body'] = view.render('head')
            else:
                ret['headers'] = [ ('Content-Type', 'application/json; charset=utf-8') ]
                ret['body'] = json.dumps(self.data)
        return ret
