from core.view import view
from core.functions import functions
import os


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

    def __init__(self, metadata):
        from core.app import app
        for key, value in metadata.items():
            if key in self.data:
                head.data = value

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
            titulo = head.data['title'][0, 75]

        head.data['title'] = titulo

        # logo = logo_model::getById(3)
        # head.data['logo'] = image::generar_url(logo['foto'][0], 'panel_max')
        # if (isset(metadata['image'])) {
        #   head.data['image_url'] = metadata['image']
        #  head.data['image'] = true
        # }
        # logo = logo_model::getById(1)
        # head.data['favicon'] = image::generar_url(logo['foto'][0], 'favicon')

        head.data['manifest_url'] = app.get_url() + 'manifest.js'


    def normal():
        from core.app import app
        if app.post.getfirst("ajax") is not None
        if (!isset($_POST['ajax']))
            if (isset($_POST['ajax_header'])) 
                $this->ajax();
             else 
                $this->data['css'] = view::css(true);
                view::set_array($this->data);
                view::render('head');
            
        
    

    def ajax():
    {
        header('Content-Type: application/json');
        echo json_encode($this->data);
        exit;
    }