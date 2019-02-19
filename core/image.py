from pathlib import Path
from os import remove
from core.app import app


class image:
    types = ["image/webp", "image/bmp", "image/gif", "image/pjpeg", "image/jpeg", "image/svg+xml", "image/png", "video/webm", "video/mp4", "application/zip", "application/x-zip-compressed", "application/octet-stream", "application/postscript", "application/msword", "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.openxmlformats-officedocument.spreadsheetml.template", "application/vnd.openxmlformats-officedocument.presentationml.template",
             "application/vnd.openxmlformats-officedocument.presentationml.slideshow", "application/vnd.openxmlformats-officedocument.presentationml.presentation", "application/vnd.openxmlformats-officedocument.presentationml.slide", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template", "application/vnd.ms-excel.addin.macroEnabled.12", "application/vnd.ms-excel.sheet.binary.macroEnabled.12", "application/pdf", "application/download"]
    extensions = ["webp", "bmp", "ico", "gif", "jpeg", "jpg", "svg", "xml", "png", "webm", "mp4", "zip", "doc",
                  "docx", "dotx", "xls", "xlsx", "xltx", "xlam", "xlsb", "ppt", "pptx", "potx", "ppsx", "sldx", "pdf"]
    upload_dir = ''
    upload_url = ''

    @staticmethod
    def get_recortes(modulo):
        moduloconfiguracion = moduloconfiguracion_model.getByModulo(modulo)
        var                 = {'idmoduloconfiguracion' : moduloconfiguracion[0]}
        if 'tipo' in app.get:
            var['tipo'] = app.get['tipo']

        modulo     = modulo_model.getAll(var, {'limit':1})
        recortes   = []
        recortes.append({'tag' : 'thumb', 'titulo' : 'Thumb', 'ancho' : 200, 'alto' : 200, 'calidad' : 90, 'tipo' : 'centrar'})
        recortes.append({'tag' : 'zoom', 'titulo' : 'Zoom', 'ancho' : 600, 'alto' : 600, 'calidad' : 90, 'tipo' : 'centrar'})
        recortes.append({'tag' : 'color', 'titulo' : 'Color', 'ancho' : 30, 'alto' : None, 'calidad' : 99, 'tipo' : 'recortar'})

        if (isset(modulo[0]['recortes'])) {
            foreach (modulo[0]['recortes'] as key => recorte) {
                recorte['ancho']   = (int) recorte['ancho']
                recorte['alto']    = (int) recorte['alto']
                recorte['calidad'] = (int) recorte['calidad']
                if (recorte['calidad'] > 100) {
                    recorte['calidad'] = 100
                }

                if (recorte['calidad'] < 0) {
                    recorte['calidad'] = 0
                }

                recortes[] = recorte
            }
        }

        return recortes
    }

    @staticmethod
    def delete(folder, file='', subfolder='', sub=''):
        import shutil
        if "" == file and '' != subfolder:
            url = image.get_upload_dir() + folder + '/' + subfolder + '/'
            my_file = Path(url)
            if my_file.is_dir():
                shutil.rmtree(url)
        elif '' == file and '' == subfolder:
            url = image.get_upload_dir() + folder + '/'
            my_file = Path(url)
            if my_file.is_dir():
                shutil.rmtree(url)
        else:
            recortes = image.get_recortes(folder)
            if '' != subfolder:
                subfolder += '/'
            if '' != sub:
                sub += '/'
            url = image.get_upload_dir() + folder + '/' + \
                subfolder + sub + file['url']
            my_file = Path(url)
            if my_file.is_file():
                my_file.unlink()

            for recorte in recortes:
                url = image.get_upload_dir() + folder + '/' + subfolder + sub + \
                    image.nombre_archivo(file['url'], recorte['tag'])
                my_file = Path(url)
                if my_file.is_file():

                    my_file.unlink()

                url = image.get_upload_dir() + folder + '/' + subfolder + sub + \
                    image.nombre_archivo(file['url'], recorte['tag'], 'webp')

                my_file = Path(url)
                if my_file.is_file():

                    my_file.unlink()


    @staticmethod
    def get_upload_dir():
        if ('' == image.upload_dir):
            image.upload_dir = app.get_dir(True) + 'uploads/img/'
        return image.upload_dir
    