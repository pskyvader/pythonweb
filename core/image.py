from pathlib import Path
from os import rename
from os import makedirs
from .app import app
from .functions import functions


class image:
    types = ["image/webp", "image/bmp", "image/gif", "image/pjpeg", "image/jpeg", "image/svg+xml", "image/png", "video/webm", "video/mp4", "application/zip", "application/x-zip-compressed", "application/octet-stream", "application/postscript", "application/msword", "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.openxmlformats-officedocument.spreadsheetml.template", "application/vnd.openxmlformats-officedocument.presentationml.template",
             "application/vnd.openxmlformats-officedocument.presentationml.slideshow", "application/vnd.openxmlformats-officedocument.presentationml.presentation", "application/vnd.openxmlformats-officedocument.presentationml.slide", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template", "application/vnd.ms-excel.addin.macroEnabled.12", "application/vnd.ms-excel.sheet.binary.macroEnabled.12", "application/pdf", "application/download"]
    extensions = ["webp", "bmp", "ico", "gif", "jpeg", "jpg", "svg", "xml", "png", "webm", "mp4", "zip", "doc",
                  "docx", "dotx", "xls", "xlsx", "xltx", "xlam", "xlsb", "ppt", "pptx", "potx", "ppsx", "sldx", "pdf"]
    upload_dir = ''
    upload_url = ''

    @classmethod
    def upload_tmp(cls, modulo):
        '''Subir a carpeta temporal, durante la creacion de la seccion. al guardar el archivo se mueve a la carpeta definitiva'''
        respuesta = {'exito': False, 'mensaje': ''}
        if 'file' in app.post:
            files = app.post['files']
            recortes = cls.get_recortes(modulo)
            archivos = []

            if 'file' in files:
                file_ary =files # functions.reArrayFiles(files['file'])
            else:
                file_ary = files

            for files in file_ary:
                archivo = cls.upload(files, 'tmp')
                respuesta['exito'] = archivo['exito']
                if not archivo['exito']:
                    respuesta['mensaje'] = archivo['mensaje']
                    break
                else:
                    recorte = cls.recortes_foto(archivo, recortes)
                    if not recorte['exito']:
                        respuesta['mensaje'] = recorte['mensaje']
                        break
                    else:
                        name = cls.nombre_archivo(archivo['name'], 'thumb')
                        archivo['url'] = cls.get_upload_url() + archivo['folder'] + '/' + name
                        respuesta['mensaje'] += archivo['original_name'] + ' <br/>'
                        archivos.append(archivo)
            respuesta['archivos'] = archivos
        else:
            respuesta['mensaje'] = 'No se encuentran archivos a subir'
        return respuesta

    @staticmethod
    def regenerar(file):
        '''regenerar imagenes ya guardadas'''
        from glob import glob
        from os import remove
        recortes       = image.get_recortes(file['folder'])
        file['name']   = file['url']
        file['folder'] = file['folder'] + '/' + file['parent'] + '/' + file['subfolder']
        for fl in glob(image.get_upload_dir() + file['folder'] + "/" + file['id'] + "-*.*"):
            remove(fl)
        respuesta = image.recortes_foto(file, recortes)
        return respuesta
    

    @staticmethod
    def move(file, folder, subfolder, name_final, folder_tmp='tmp'):
        '''mover archivo (normalmente) desde la carpeta temporal a la definitiva'''
        recortes = image.get_recortes(folder)
        folder_tmp = image.get_upload_dir() + folder_tmp
        base_folder = image.get_upload_dir() + folder
        folder = base_folder + '/' + name_final + '/' + subfolder

        my_file = Path(folder)
        if not my_file.is_dir():
            makedirs(folder, 777)

        name = file['tmp'].split('.')
        extension = (name.pop()).lower()

        file['url'] = file['id'] + '.' + extension
        rename(folder_tmp + '/' + file['tmp'], folder + '/' + file['url'])

        for recorte in recortes:
            rename(folder_tmp + '/' + image.nombre_archivo(
                file['tmp'], recorte['tag']), folder + '/' + image.nombre_archivo(file['url'], recorte['tag']))
            my_file = Path(
                folder_tmp + '/' + image.nombre_archivo(file['tmp'], recorte['tag'], 'webp'))
            if not my_file.is_dir():
                rename(
                    folder_tmp + '/' +
                    image.nombre_archivo(file['tmp'], recorte['tag'], 'webp'),
                    folder + '/' + image.nombre_archivo(file['url'], recorte['tag'], 'webp'))

        del file['tmp']
        file['subfolder'] = subfolder
        return file
    @staticmethod
    def copy(original_file, id_final, folder, subfolder = "", name_final = "", tag = 'thumb'):
        """Copia un archivo y retorna la informacion del archivo nuevo """
        import os
        respuesta = {'exito' : False, 'mensaje' : ''}

        name      = original_file['url'].split('.')
        extension = (name.pop()).lower()

        new_file = {'portada': True, 'id': 1, 'url': id_final + '.' + extension, 'parent': name_final, 'folder': folder, 'subfolder': subfolder, 'tmp': ''}
        original = image.generar_dir(original_file, tag);

        if original != '':
            base_folder = image.get_upload_dir() + folder
            folder      = base_folder;
            if name_final != '':
                folder += '/' + name_final
            
            if subfolder != '':
                folder += '/' + subfolder;
            
            my_file = Path(folder)
            if not my_file.is_dir():
                makedirs(folder, 777)
                
            destino = folder + '/' + new_file['url'];
            if os.access(dir_resources, os.R_OK):
            if (is_writable(folder)) {
                copy(original, destino);
                respuesta['exito'] = true;
                respuesta['file']  = array(new_file);
            } else {
                respuesta['mensaje'] = 'La carpeta ' . folder . ' no tiene permisos de escritura';
            }
        } else {
            respuesta['mensaje'] = 'El archivo original no existe';
        }
        return respuesta;
    }

    @staticmethod
    def get_recortes(modulo):
        #moduloconfiguracion = moduloconfiguracion_model.getByModulo(modulo)
        moduloconfiguracion = [1]
        var = {'idmoduloconfiguracion': moduloconfiguracion[0]}
        if 'tipo' in app.get:
            var['tipo'] = app.get['tipo']

        #modulo     = modulo_model.getAll(var, {'limit':1})
        modulo = {}
        recortes = []
        recortes.append({'tag': 'thumb', 'titulo': 'Thumb', 'ancho': 200,
                         'alto': 200, 'calidad': 90, 'tipo': 'centrar'})
        recortes.append({'tag': 'zoom', 'titulo': 'Zoom', 'ancho': 600,
                         'alto': 600, 'calidad': 90, 'tipo': 'centrar'})
        recortes.append({'tag': 'color', 'titulo': 'Color', 'ancho': 30,
                         'alto': None, 'calidad': 99, 'tipo': 'recortar'})

        if 0 in modulo and 'recortes' in modulo[0]:
            for recorte in modulo[0]['recortes']:
                recorte['ancho'] = int(recorte['ancho'])
                recorte['alto'] = int(recorte['alto'])
                recorte['calidad'] = int(recorte['calidad'])
                if recorte['calidad'] > 100:
                    recorte['calidad'] = 100

                if recorte['calidad'] < 0:
                    recorte['calidad'] = 0

                recortes.append(recorte)
        return recortes

    @staticmethod
    def nombre_archivo(file, tag='', extension='', remove=False):
        name = file.split('.')
        if ('' == extension):
            extension = (name.pop()).lower()
        else:
            name.pop()

        if remove:
            name = (''.join(name)).split('-')
            if len(name) > 1:
                name.pop()

        name = functions.url_amigable(''.join(name))
        if '' != tag:
            return name + '-' + tag + '.' + extension
        else:
            return name + '.' + extension

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
    def delete_temp():
        from os import listdir
        from os.path import getmtime
        from datetime import datetime
        now = datetime.now()
        horas = 1

        carpeta = image.get_upload_dir() + 'tmp/'  # ruta actual
        # obtenemos un archivo y luego otro sucesivamente
        for archivo in listdir(carpeta):
            my_file = Path(carpeta + archivo)
            if my_file.is_file():  # verificamos si es o no un archivo
                # si el archivo fue creado hace más de horas, borrar
                if ((now - getmtime(carpeta + archivo)) / 3600 > horas):
                    my_file.unlink()

    @staticmethod
    def get_upload_dir():
        if ('' == image.upload_dir):
            image.upload_dir = app.get_dir(True) + 'uploads/img/'
        return image.upload_dir
