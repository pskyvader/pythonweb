class head:
    data = {
        'favicon': '',
        'keywords': False,
        'keywords_text': '',
        'description': False,
        'description_text': '',
        'title': '',
        'current_url': '',
        'image': False,
        'image_url': '',
        'logo': '',
        'color_primario': '',
        'manifest_url': '',
        'path': '',
        'modulo': '',
        'max_size': -1,
    }

    metadata={}

    def __init__(self, metadata):
        from core.app import app
        from core.functions import functions
        head_tmp={}
        for key, value in metadata.items():
            if key in self.data:
                head_tmp = value

        config = app.get_config()
        
        head_tmp={}
        head_tmp['current_url'] = functions.current_url()
        head_tmp['path'] = app.path
        head_tmp['color_primario'] = config['color_primario']
        head_tmp['googlemaps_key'] = config['googlemaps_key']
        # size=functions::get_max_size()
        #head_tmp['max_size'] = size
        # head_tmp['max_size_format'] = (size<0)?"Ilimitado":functions::file_size(size,true)

        titulo = head_tmp['title'] + ' - ' + config['title']
        if (len(titulo) > 75):
            titulo = head_tmp['title'] + ' - ' + config['short_title']

        if (len(titulo) > 75):
            titulo = head_tmp['title']

        if (len(titulo) > 75):
            titulo = head_tmp['title'][0, 75]

        head.metadata['title'] = titulo

        # logo = logo_model::getById(3)
        # head_tmp['logo'] = image::generar_url(logo['foto'][0], 'panel_max')
        # if (isset(metadata['image'])) {
        #   head_tmp['image_url'] = metadata['image']
        #  head_tmp['image'] = true
        # }
        # logo = logo_model::getById(1)
        # head_tmp['favicon'] = image::generar_url(logo['foto'][0], 'favicon')

        head_tmp['manifest_url'] = app.get_url() + 'manifest.js'

        for key, value in head_tmp.items():
            if key not in head.metadata:
                head.metadata = value

        for key, value in head.data.items():
            if key not in head.metadata:
                head.metadata = value





    def normal(self):
        from core.app import app
        from core.view import view
        import json
        
        ret={'headers':'','body':''}
        if app.post.getfirst("ajax") is not None:
            if app.post.getfirst("ajax_header") is not None:
                ret['headers']='Content-Type: application/json'
                ret['body']=json.dumps(self.data)
            else:
                self.data['css']=view.css(True)
                view.add_array(self.data)
                ret['body']=view.render('head')
        
        return ret