from core.image import image
from core.file import file
from core.functions import functions


class product_detail:
    producto = None
    url = []

    def __init__(self, producto, url):
        self.producto = producto
        self.url = url

    def galeria(recorte="foto1"):
        lista_imagenes = []
        thumb = []
        for foto in self.producto["foto"]:
            li = {"srcset": []}
            th = {}
            # li['title'] = self.producto['titulo']
            li["image"] = image.generar_url(foto, recorte)
            li["thumb"] = th["thumb"] = image.generar_url(foto, "cart")
            th["url"] = image.generar_url(foto, "")
            src = image.generar_url(foto, recorte, "webp")
            if src != "":
                li["srcset"].append({"media": "", "src": src, "type": "image/webp"})

            if li["image"] != "":
                lista_imagenes.append(li)
                thumb.append(th)

        data = {}
        data["lista_imagenes"] = lista_imagenes
        data["thumb"] = thumb
        return data
        
    def tabs(self):
        extra=''
        if len(self.producto['archivo']) > 0:
            files = []
            for a in self.producto['archivo']:
                files.append({'title' : a['url'], 'size' : functions.file_size(file.generar_dir(a, '')), 'url' : file.generar_url(a, '')})
            
            data={}
            data['files']= files
            data['title']= 'Archivos'
            extra=('files',data.copy())
        
        
        data={}
        is_description=(functions.remove_tags(self.producto['descripcion'])!='')
        data['description']= self.producto['descripcion']
        
        data['extra']= extra
        if is_description or extra!='':
            tabs=('product/tabs',data)
        else:
            tabs=""
        
        return tabs
    
