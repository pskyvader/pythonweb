from pathlib import Path
from .image import image
from .app import app


class file(image):
    types = ["application/zip", "application/x-zip-compressed", "application/octet-stream", "application/postscript", "application/msword", "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.openxmlformats-officedocument.spreadsheetml.template", "application/vnd.openxmlformats-officedocument.presentationml.template", "application/vnd.openxmlformats-officedocument.presentationml.slideshow",
             "application/vnd.openxmlformats-officedocument.presentationml.presentation", "application/vnd.openxmlformats-officedocument.presentationml.slide", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template", "application/vnd.ms-excel.addin.macroEnabled.12", "application/vnd.ms-excel.sheet.binary.macroEnabled.12", "application/pdf", "application/download"]
    extensions = ["zip", "doc", "docx", "dotx", "xls", "xlsx", "xltx",
                  "xlam", "xlsb", "ppt", "pptx", "potx", "ppsx", "sldx", "pdf"]

    @staticmethod
    def upload_tmp(modulo):
        '''Subir a carpeta temporal, durante la creacion de la seccion. al guardar el archivo se mueve a la carpeta definitiva'''
        respuesta = {'exito': False, 'mensaje': ''}

        if 'file' in app.post:
            files = app.post['files']
            archivos = []

            if 'file' in files:
                file_ary = files  # functions.reArrayFiles(files['file'])
            else:
                file_ary = files

            for files in file_ary:
                archivo = file.upload(files, 'tmp')
                respuesta['exito'] = archivo['exito']
                if not archivo['exito']:
                    respuesta['mensaje'] = archivo['mensaje']
                    break
                else:
                    name = file.nombre_archivo(archivo['name'], '')
                    archivo['url'] = file.get_upload_url(
                    ) + archivo['folder'] + '/' + name
                    respuesta['mensaje'] += archivo['original_name'] + ' <br/>'
                    archivos.append(archivo)
            respuesta['archivos'] = archivos
        else:
            respuesta['mensaje'] = 'No se encuentran archivos a subir'
        return respuesta

    @staticmethod
    def delete(folder, file_name='', subfolder='', sub=''):
        import shutil
        if "" == file_name and '' != subfolder:
            url = file.get_upload_dir() + folder + '/' + subfolder + '/'
            my_file = Path(url)
            if my_file.is_dir():
                shutil.rmtree(url)
        elif '' == file_name and '' == subfolder:
            url = file.get_upload_dir() + folder + '/'
            my_file = Path(url)
            if my_file.is_dir():
                shutil.rmtree(url)
        else:
            if '' != subfolder:
                subfolder += '/'

            if '' != sub:
                sub += '/'

            url = file.get_upload_dir() + folder + '/' + \
                subfolder + sub + file_name['url']
            my_file = Path(url)
            if my_file.is_file():
                my_file.unlink()
