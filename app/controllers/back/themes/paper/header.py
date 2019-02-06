from core.functions import functions
from core.view import view
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
        from core.app import app
        for key, value in metadata.items():
            if key in self.data:
                head.data[key] = value

        config = app.get_config()
        head.data['current_url'] = functions.current_url()
        head.data['path'] = app.path
        head.data['color_primario'] = config['color_primario']
        head.data['googlemaps_key'] = config['googlemaps_key']
        # size=functions.get_max_size()
        #head.data['max_size'] = size
        # head.data['max_size_format'] = (size<0)?"Ilimitado":functions.file_size(size,true)

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
        # logo = logo_model.getById(3)
        # head.data['image']=image.generar_url(logo['foto'][0], 'panel_max')
        # }
        # logo = logo_model.getById(1)
        # head.data['favicon'] = image.generar_url(logo['foto'][0], 'favicon')

        head.data['manifest_url'] = app.get_url() + 'manifest.js'

    def normal(self):
        from core.app import app
        import json

        ret = {'headers': '', 'body': ''}
        if app.post.getfirst("ajax") is None:
            if app.post.getfirst("ajax_header") is None:
                self.data['css'] = view.css(True)
                view.add_array(self.data)
                ret['body'] = view.render('head')
            else:
                ret['headers'] = 'Content-Type: application/json'
                ret['body'] = json.dumps(self.data)
        return ret



class header:
    data = { 'logo' : '', 'url_exit' : '', }
    def normal(self):
        from core.app import app
        import datetime
        ret={'body':''}
        if app.post.getfirst("ajax") is None:
            #logo = logo_model.getById(3);
            #self.data['logo_max'] = image.generar_url(logo['foto'][0], 'panel_max');
            #logo = logo_model.getById(4);
            #self.data['logo_min'] = image.generar_url(logo['foto'][0], 'panel_min');
            self.data['url_exit'] = functions.generar_url(['logout'], False);
            view.add_array(self.data);
            view.add('date', datetime.datetime.today().strftime('%Y-%m-%d'));
            ret['body']=view.render('header');
        return ret
        
    

