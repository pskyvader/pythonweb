
from app.models.seccion import seccion as seccion_model
from core.file import file
from core.functions import functions
from core.view import view

class cms(base):
    def __init__(self):
        super().__init__(app.get['idseo'])
        
    def index(self):
        ret = {'body': []}
        self.meta(self.seo)
        url_return = functions.url_redirect(self.url)
        if url_return != '':
            ret['error'] = 301
            ret['redirect'] = url_return
            return ret

        h = head(self.metadata)
        ret_head = h.normal()
        if ret_head['headers'] != '':
            return ret_head
        ret['body'] += ret_head['body']

        he = header()
        ret['body'] += he.normal()['body']

        ba = banner()
        ret['body'] += ba.individual(self.seo['banner'], self.metadata['title'], self.seo['subtitulo'])['body']

        bc = breadcrumb()
        ret['body'] += bc.normal(self.breadcrumb)['body']

        var = array()
        if self.seo['tipo_modulo'] != 0:
            var['tipo'] = self.seo['tipo_modulo']
        
        if self.modulo['hijos']:
            var['idpadre'] = 0
        
        row     = seccion_model.getAll(var)
        sidebar = []
        for s in row:
            sidebar.append({'title' : s['titulo'], 'active' : '', 'url' : functions.url_seccion([self.url[0], 'detail'], s)})
        
        data={}

        data['title_category']= self.seo['titulo']
        data['sidebar']= sidebar

        data['description']= ''
        ret['body'].append(('cms-sidebar',data))
        f = footer()
        ret['body'] += f.normal()['body']
    

    def detail(self,var = []):
        if len(var)>0:
            id      = functions.get_idseccion(var[0])
            seccion = seccion_model.getById(id)
            if isset(seccion[0]):
                self.url          = functions.url_seccion([self.url[0], 'detail'], seccion, true)
                self.breadcrumb.append({'url' : functions.generar_url(self.url), 'title' : seccion['titulo']})
            

        url_return = functions.url_redirect(self.url)
        if url_return != '':
            ret['error'] = 301
            ret['redirect'] = url_return
            return ret

        self.meta(seccion)

        h = head(self.metadata)
        ret_head = h.normal()
        if ret_head['headers'] != '':
            return ret_head
        ret['body'] += ret_head['body']

        he = header()
        ret['body'] += he.normal()['body']


        ba = banner()
        ret['body'] += ba.individual(self.seo['banner'], self.seo['subtitulo'])['body']

        bc = breadcrumb()
        ret['body'] += bc.normal(self.breadcrumb)['body']
        

        var = {}
        if self.seo['tipo_modulo'] != 0:
            var['tipo'] = self.seo['tipo_modulo']
        
        if self.modulo['hijos']:
            var['idpadre'] = 0
        
        row     = seccion_model.getAll(var)
        sidebar = []
        foreach (row as key : s:
            sidebar.append({'title' : s['titulo'], 'active' : '', 'url' : functions.url_seccion([self.url[0], 'detail'], s)})
        

        extra=''
        if count(seccion['archivo']) > 0:
            files = array()
            foreach (seccion['archivo'] as key : a:
                files[] = array('title' : a['url'], 'size' : functions.file_size(file.generar_dir(a, '')), 'url' : file.generar_url(a, ''))
            
            view.set('files', files)
            view.set('title', 'Archivos')
            extra=view.render('files',false,true)
        

        view.set('sidebar', sidebar)
        view.set('title_category', self.seo['titulo'])
        view.set('title', seccion['titulo'])
        view.set('description', seccion['descripcion'])
        view.set('extra', extra)
        view.render('cms-sidebar')

        footer = new footer()
        footer->normal()
    

