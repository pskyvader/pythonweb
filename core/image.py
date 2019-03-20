from pathlib import Path
from os import makedirs
from os import rename
from .app import app
from .functions import functions


class image:
    types = ["image/webp", "image/bmp", "image/gif", "image/pjpeg", "image/jpeg", "image/svg+xml", "image/png", "video/webm", "video/mp4", "application/zip", "application/x-zip-compressed", "application/octet-stream", "application/postscript", "application/msword", "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.openxmlformats-officedocument.spreadsheetml.template", "application/vnd.openxmlformats-officedocument.presentationml.template",
             "application/vnd.openxmlformats-officedocument.presentationml.slideshow", "application/vnd.openxmlformats-officedocument.presentationml.presentation", "application/vnd.openxmlformats-officedocument.presentationml.slide", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template", "application/vnd.ms-excel.addin.macroEnabled.12", "application/vnd.ms-excel.sheet.binary.macroEnabled.12", "application/pdf", "application/download"]
    extensions = [".webp", ".bmp", ".ico", ".gif", ".jpeg", ".jpg", ".svg", ".xml", ".png", ".webm", ".mp4", ".zip", ".doc",
                  ".docx", ".dotx", ".xls", ".xlsx", ".xltx", ".xlam", ".xlsb", ".ppt", ".pptx", ".potx", ".ppsx", ".sldx", ".pdf"]
    upload_dir = ''
    upload_url = ''

    @staticmethod
    def upload_tmp(modulo):
        '''Subir a carpeta temporal, durante la creacion de la seccion. al guardar el archivo se mueve a la carpeta definitiva'''
        respuesta = {'exito': False, 'mensaje': ''}
        if 'file' in app.post:
            files = app.post['files']
            recortes = image.get_recortes(modulo)
            archivos = []

            if 'file' in files:
                file_ary = files  # functions.reArrayFiles(files['file'])
            else:
                file_ary = files

            for files in file_ary:
                archivo = image.upload(files, 'tmp')
                respuesta['exito'] = archivo['exito']
                if not archivo['exito']:
                    respuesta['mensaje'] = archivo['mensaje']
                    break
                else:
                    recorte = image.recortes_foto(archivo, recortes)
                    if not recorte['exito']:
                        respuesta['mensaje'] = recorte['mensaje']
                        break
                    else:
                        name = image.nombre_archivo(archivo['name'], 'thumb')
                        archivo['url'] = image.get_upload_url(
                        ) + archivo['folder'] + '/' + name
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
        recortes = image.get_recortes(file['folder'])
        file['name'] = file['url']
        file['folder'] = file['folder'] + '/' + \
            file['parent'] + '/' + file['subfolder']
        for fl in glob(image.get_upload_dir() + file['folder'] + "/" + file['id'] + "-*.*"):
            remove(fl)
        respuesta = image.recortes_foto(file, recortes)
        return respuesta

    @staticmethod
    def move(file, folder, subfolder, name_final, folder_tmp='tmp'):
        '''mover archivo (normalmente) desde la carpeta temporal a la definitiva'''
        from os.path import splitext

        recortes = image.get_recortes(folder)
        folder_tmp = image.get_upload_dir() + folder_tmp
        base_folder = image.get_upload_dir() + folder
        folder = base_folder + '/' + name_final + '/' + subfolder

        my_file = Path(folder)
        if not my_file.is_dir():
            makedirs(folder, 777)

        name,extension=splitext(file['tmp'])

        file['url'] = file['id'] + extension
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
    def copy(original_file, id_final, folder, subfolder="", name_final="", tag='thumb'):
        """Copia un archivo y retorna la informacion del archivo nuevo """
        import os
        from shutil import copyfile
        respuesta = {'exito': False, 'mensaje': ''}

        name,extension=os.path.splitext(original_file['url'])

        new_file = {'portada': True, 'id': 1, 'url': str(id_final) + extension, 'parent': name_final, 'folder': folder, 'subfolder': subfolder, 'tmp': ''}
        original = image.generar_dir(original_file, tag)

        if original != '':
            base_folder = image.get_upload_dir() + folder
            folder = base_folder
            if name_final != '':
                folder += '/' + name_final

            if subfolder != '':
                folder += '/' + subfolder

            my_file = Path(folder)
            if not my_file.is_dir():
                makedirs(folder, 777)

            destino = folder + '/' + new_file['url']
            if os.access(folder, os.W_OK):
                copyfile(original, destino)
                respuesta['exito'] = True
                respuesta['file'] = [new_file]
            else:
                respuesta['mensaje'] = 'La carpeta ' + \
                    folder + ' no tiene permisos de escritura'
        else:
            respuesta['mensaje'] = 'El archivo original no existe'

        return respuesta

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
    def upload(file, folder_upload='tmp', name_final=''):
        """subir archivo"""
        import uuid
        import stat
        import os
        folder = image.get_upload_dir() + folder_upload

        respuesta = image.validate(file)
        if respuesta['exito']:
            if '' == name_final:
                name_final = uuid.uuid4().hex
            else:
                name_final,extension=os.path.splitext(name_final)
                name_final = functions.url_amigable(''.join(name_final))
            
            name,extension=os.path.splitext(file['name'])
            extension=extension.lower()

            my_file = Path(folder)
            if not my_file.is_dir():
                makedirs(folder, 777)

            #respuesta['exito'] = move_uploaded_file(file['tmp_name'], folder + '/' + name_final + extension)
            respuesta['exito'] = rename(
                file['tmp_name'], folder + '/' + name_final + extension)
            if not respuesta['exito']:
                respuesta['mensaje'] = "Error al mover archivo. Permisos: " + \
                    oct(stat.S_IMODE(os.lstat(folder).st_mode)) + \
                    ", carpeta: " + folder
            else:
                respuesta['name'] = name_final + extension
                respuesta['folder'] = folder_upload
                respuesta['original_name'] = file['name']
                respuesta['mensaje'] = "Imagen " + \
                    file['name'] + " Subida correctamente"
        return respuesta

    @classmethod
    def validate(cls, file):
        from os.path import splitext
        name,extension=splitext(file['name'])
        respuesta = {'exito': False, 'mensaje': 'Error: formato no valido'}
        if 0 != file['error']:
            respuesta['mensaje'] = 'Error al subir archivo: ' + file['error']
        elif file['type'] not in cls.types:
            respuesta['mensaje'] += '. Extension: ' + file['type']
        elif extension not in cls.extensions:
            respuesta['mensaje'] += '.<br/> Extension de archivo: ' + extension
        else:
            respuesta['exito'] = True
        return respuesta

    @staticmethod
    def recortes_foto(archivo, recortes_foto):
        """Genera recortes de las fotos"""
        from PIL import Image
        respuesta = {'exito': False}
        ruta = image.get_upload_dir() + archivo['folder']
        foto = archivo['name']
        ruta_imagen = ruta + '/' + foto
        my_file = Path(ruta_imagen)
        if not my_file.is_file():
            respuesta['mensaje'] = 'Archivo ' + ruta_imagen + ' no existe'
            return respuesta

        im = Image.open(ruta_imagen)
        ancho, alto = im.size

        ancho_maximo = 0
        alto_maximo = 0
        ancho_valido = 0
        alto_valido = 0

        for recorte in recortes_foto:
            if recorte['ancho']!=None and recorte['ancho'] > ancho_maximo:
                ancho_maximo = recorte['ancho']
                if ancho_maximo > ancho_valido and ancho_maximo <= ancho:
                    ancho_valido = ancho_maximo
            if recorte['alto']!=None and recorte['alto'] > alto_maximo:
                alto_maximo = recorte['alto']
                if alto_maximo > alto_valido and alto_maximo <= alto:
                    alto_valido = alto_maximo

        # si es valido, se crea una imagen intermedia para acelerar el proceso de recorte de las demas imagenes
        if (alto > (alto_valido * 1.5) and alto_valido > 0) or (ancho > (ancho_valido * 1.5) and ancho_valido > 0):
            # alto proporcional segun mayor ancho valido
            #alto_final = (alto / ancho) * ancho_valido
            # ancho proporcional segun mayor alto valido
            ancho_final = (ancho / alto) * alto_valido
            if ancho_final >= ancho_valido:
                respuesta = image.recortar_foto( {'tag': 'recorte_previo', 'ancho': None, 'alto': alto_valido, 'calidad': 100, 'tipo': 'rellenar'}, archivo)
            else:
                respuesta = image.recortar_foto( {'tag': 'recorte_previo', 'ancho': ancho_valido, 'alto': None, 'calidad': 100, 'tipo': 'rellenar'}, archivo)

            if not respuesta['exito']:
                return respuesta

            archivo_recorte = archivo
            archivo_recorte['name'] = image.nombre_archivo(archivo_recorte['name'], 'recorte_previo')
            for recorte in recortes_foto:
                if recorte['ancho']!=None and recorte['ancho'] <= ancho_valido and recorte['alto']!=None and recorte['alto'] <= alto_valido:
                    respuesta = image.recortar_foto(recorte, archivo_recorte)
                else:
                    respuesta = image.recortar_foto(recorte, archivo)

                if not respuesta['exito']:
                    return respuesta

        else:
            for recorte in recortes_foto:
                respuesta = image.recortar_foto(recorte, archivo)
                if not respuesta['exito']:
                    return respuesta

        return respuesta

    @staticmethod
    def proporcion_foto(ancho_maximo, alto_maximo, ancho, alto, tipo):
        """Obtener proporciones de foto final"""
        proporcion_imagen = ancho / alto
        proporcion_miniatura = ancho_maximo / alto_maximo
        miniatura_ancho = ancho_maximo
        miniatura_alto = alto_maximo

        if tipo == 'recortar':
            if proporcion_imagen > proporcion_miniatura:
                miniatura_ancho = alto_maximo * proporcion_imagen
            elif proporcion_imagen < proporcion_miniatura:
                miniatura_alto = ancho_maximo / proporcion_imagen

            x = (miniatura_ancho - ancho_maximo) / 2
            y = (miniatura_alto - alto_maximo) / 2
        else:
            if proporcion_imagen > proporcion_miniatura:
                if ancho > alto:
                    miniatura_alto = ancho_maximo / proporcion_imagen
                else:
                    if ancho_maximo > alto_maximo:
                        miniatura_alto = alto_maximo * proporcion_imagen
                    else:
                        miniatura_alto = ancho_maximo / proporcion_imagen

            elif proporcion_imagen < proporcion_miniatura:
                if ancho_maximo > alto_maximo:
                    miniatura_ancho = alto_maximo * proporcion_imagen
                elif ancho_maximo < alto_maximo:
                    miniatura_ancho = ancho_maximo * proporcion_miniatura
                else:
                    miniatura_ancho = ancho_maximo * proporcion_imagen

            if tipo == 'centrar' and ancho < miniatura_ancho and alto < miniatura_alto:
                x = (ancho_maximo - ancho) / 2
                y = (alto_maximo - alto) / 2
            else:
                x = (ancho_maximo - miniatura_ancho) / 2
                y = (alto_maximo - miniatura_alto) / 2

        return int(x), int(y), int(miniatura_ancho),  int(miniatura_alto)

    @staticmethod
    def recortar_foto(recorte, datos):
        """Recorta una foto"""
        from PIL import Image
        respuesta = {'exito': False, 'mensaje': 'error al recortar imagen'}
        ancho_maximo = recorte['ancho']
        alto_maximo = recorte['alto']
        ruta = image.get_upload_dir() + datos['folder'] + '/'
        foto = datos['name']
        etiqueta = recorte['tag']
        tipo = recorte['tipo']

        ruta_imagen = ruta + foto
        my_file = Path(ruta_imagen)
        if not my_file.is_file():
            respuesta['mensaje'] = 'Archivo ' + ruta_imagen + ' no existe'
            return respuesta

        im = Image.open(ruta_imagen)
        ancho, alto = im.size
        imagen_tipo = im.format

        proporcion_imagen = ancho / alto
        if None == ancho_maximo or 0 == ancho_maximo:
            ancho_maximo = int(round(alto_maximo * proporcion_imagen))
        if None == alto_maximo or 0 == alto_maximo:
            alto_maximo = int(round(ancho_maximo / proporcion_imagen))

        x, y, miniatura_ancho, miniatura_alto = image.proporcion_foto(
            ancho_maximo, alto_maximo, ancho, alto, tipo)

        if tipo == "recortar":
            box = (x, y, ancho_maximo+x, alto_maximo+y)
            im.thumbnail((miniatura_ancho, miniatura_alto))
            new_im = im.crop(box)
        elif "rellenar" == tipo:
            new_im = Image.new( 'RGBA', (miniatura_ancho, miniatura_alto), (255, 255, 255, 0))
            box = (x, y)
            new_im.paste(im.resize((miniatura_ancho, miniatura_alto)), (box))
        else:
            if ancho >= miniatura_ancho or alto >= miniatura_alto:
                new_im = Image.new( 'RGBA', (miniatura_ancho, miniatura_alto), (255, 255, 255, 0))
                box = (x, y)
                #im=im.resize((miniatura_ancho, miniatura_alto))
                print(box,etiqueta,new_im.size,im.size)
                new_im.paste(im, (box))
            else:
                new_im = Image.new( 'RGBA', (ancho_maximo, alto_maximo), (255, 255, 255, 0))
                box = (x, y, miniatura_ancho+x, miniatura_alto+y)
                print(box,etiqueta)
                new_im.paste(im.resize((miniatura_ancho, miniatura_alto)), (box))

        foto_recorte = image.nombre_archivo(foto, etiqueta, '', True)
        foto_webp = image.nombre_archivo(foto, etiqueta, 'webp', True)

        my_file = Path(ruta + foto_recorte)
        if my_file.is_file():
            my_file.unlink()
        my_file = Path(ruta + foto_webp)
        if my_file.is_file():
            my_file.unlink()
        

        new_im.save(ruta + foto_recorte)
        #if "png" != imagen_tipo.lower():
        new_im.save(ruta + foto_webp)

        respuesta['exito'] = True

        return respuesta

    @staticmethod
    def nombre_archivo(file, tag='', extension='', remove=False):
        from os.path import splitext
        name, ext = splitext(file)
        if'' == extension:
            extension = ext
        else:
            extension='.'+extension

        if remove:
            name = (''.join(name)).split('-')
            if len(name) > 1:
                name.pop()

        name = functions.url_amigable(''.join(name))
        if '' != tag:
            return name + '-' + tag + extension
        else:
            return name + extension

    @staticmethod
    def generar_url(file, tag='thumb', extension="", folder="", subfolder=""):
        if len(file) == 0:
            return ''

        if '' == folder:
            folder = file['folder']

        if '' != subfolder:
            subfolder += '/'
        elif file['parent'] != '':
            subfolder = str(file['parent']) + '/'
            if file['subfolder'] != '':
                subfolder += file['subfolder'] + '/'

        url = folder + '/' + subfolder + \
            image.nombre_archivo(file['url'], tag, extension)
        time = functions.fecha_archivo(image.get_upload_dir() + url, True)
        if time != False:
            archivo = image.get_upload_url() + url + '?time=' + str(time)
        else:
            archivo = ''
        return archivo

    @staticmethod
    def generar_dir(file, tag='thumb', extension="", folder="", subfolder=""):
        if '' == folder:
            folder = file['folder']
        if '' != subfolder:
            subfolder += '/'
        elif file['parent'] != '':
            subfolder = str(file['parent']) + '/'
            if file['subfolder'] != '':
                subfolder += file['subfolder'] + '/'

        url = folder + '/' + subfolder + \
            (image.nombre_archivo(file['url'], tag, extension))
        archivo = image.get_upload_dir() + url
        my_file = Path(archivo)
        if not my_file.is_file():
            archivo = ''
        return archivo

    @staticmethod
    def portada(fotos):
        portada = {}
        if len(fotos) > 0:
            portada = fotos[0]
            for f in fotos:
                if (isinstance(f['portada'], str) and 'true' == f['portada']) or (isinstance(f['portada'], bool) and f['portada']):
                    portada = f
                    break
        return portada

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
        now = functions.current_time('',False)
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

    @staticmethod
    def get_upload_url():
        if ('' == image.upload_url):
            image.upload_url = app.get_url(True) + 'uploads/img/'
        return image.upload_url
