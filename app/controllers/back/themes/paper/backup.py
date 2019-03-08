from .base import base
from app.models.administrador import administrador as administrador_model
from app.models.configuracion import configuracion as configuracion_model


from .head import head
from .header import header
from .aside import aside
from .footer import footer


from .configuracion_administrador import configuracion_administrador

from core.app import app
from core.database import database
from core.functions import functions

from pathlib import Path
import os
import json


class backup(base):
    url = ['backup']
    metadata = {'title': 'backup', 'modulo': 'backup'}
    breadcrumb = []
    base_dir = ''
    dir_backup = ''
    archivo_log = ''
    no_restore = ['backup/']

    def __init__(self):
        backup.base_dir = app.get_dir(True)
        backup.dir_backup = backup.base_dir + 'backup'
        backup.archivo_log = app.get_dir(True) + '/log.json'

    @classmethod
    def index(cls):
        '''Controlador de lista_class de elementos base, puede ser sobreescrito en el controlador de cada modulo'''
        ret = {'body': []}
        # Clase para enviar a controlador de lista_class
        url_final = cls.url.copy()

        if not administrador_model.verificar_sesion():
            url_final = ['login', 'index'] + url_final
        # verificar sesion o redireccionar a login
        url_return = functions.url_redirect(url_final)
        if url_return != '':
            ret['error'] = 301
            ret['redirect'] = url_return
            return ret

        h = head(cls.metadata)
        ret_head = h.normal()
        if ret_head['headers'] != '':
            return ret_head
        ret['body'] += ret_head['body']

        he = header()
        ret['body'] += he.normal()['body']

        asi = aside()
        ret['body'] += asi.normal()['body']

        mensaje_error = ''
        my_file = Path(cls.dir_backup)
        if my_file.is_dir():
            if os.access(cls.dir_backup, os.W_OK) is not True:
                mensaje_error = 'Debes dar permisos de escritura o eliminar el archivo ' + cls.dir_backup

        elif os.access(cls.base_dir, os.W_OK) is not True:
            mensaje_error = 'Debes dar permisos de escritura en ' + cls.base_dir

        mensaje = "Tiempo promedio de respaldo: "
        tiempo_lento = configuracion_model.getByVariable('tiempo_backup_lento')
        if isinstance(tiempo_lento, bool):
            tiempo_lento = 0
        else:
            tiempo_lento = float(tiempo_lento.replace(',', '.'))
            mensaje += str(tiempo_lento) + " segundos (servidor lento)"

        tiempo_rapido = configuracion_model.getByVariable(
            'tiempo_backup_rapido')
        if isinstance(tiempo_rapido, bool):
            tiempo_rapido = 0
        else:
            tiempo_rapido = float(tiempo_rapido.replace(',', '.'))
            if tiempo_lento > 0:
                mensaje += ", "

            mensaje += str(tiempo_rapido) + " segundos (servidor rápido)"

        row = {}
        files = []
        for root, dirs, file in os.walk(cls.dir_backup):
            for fichero in file:
                name, extension = os.path.splitext(fichero)
                if(extension == ".zip"):
                    files.append(name+extension)

        url = app.get_url(True) + 'backup/'

        for key, f in dict.fromkeys(files):
            name, extension = os.path.splitext(f)
            fecha = name.split('-')
            fecha = fecha.pop()
            row[fecha] = {
                'even': (key % 2 == 0),
                'id': fecha,
                'fecha': functions.formato_fecha(fecha),
                'size': functions.file_size(cls.dir_backup + '/' + f),
                'url': url + f,
            }

        # lista de los valores del dict, en orden inverso
        row = reversed(sorted(row.values()))
        data = {}
        data['row'] = row
        data['breadcrumb'] = cls.breadcrumb
        data['title'] = cls.metadata['title']
        data['mensaje_error'] = mensaje_error
        data['mensaje'] = mensaje
        data['tiempo_lento'] = tiempo_lento
        data['tiempo_rapido'] = tiempo_rapido

        ret['body'].append(('backup', data))

        f = footer()
        ret['body'] += f.normal()['body']
        return ret

    def restaurar(self):
        '''Restaura un backup, usar con precaucion ya que reemplaza todos los archivos de codigo'''
        ret = {'body': ''}
        import zipfile
        file = None
        tiempo = functions.current_time(as_string=False)
        respuesta = {'exito': False,
                     'mensaje': 'archivo no encontrado', 'errores': []}
        id = app.post['id']
        inicio = int(app.post['inicio']) - 1 if 'inicio' in app.post else 0

        for root, dirs, files in os.walk(self.dir_backup):
            for fichero in files:
                if id in fichero:
                    file = fichero

        if file is not None:
            file = self.dir_backup + '/' + file
            if zipfile.is_zipfile(file):
                zip = zipfile.ZipFile(file, 'r')
                file_list = zip.infolist()
                total = len(file_list)
                for i in range(inicio, total):
                    nombre = file_list[i]
                    if nombre not in self.no_restore:
                        try:
                            zip.extract(nombre, self.base_dir)
                        except:
                            respuesta['errores'].append(nombre)
                    respuesta['errores'].append(nombre)

                    if i % 100 == 0:
                        log = {'mensaje': 'Restaurando ' + nombre[-30:] + ' (' + str(
                            i + 1) + '/' + str(total) + ')', 'porcentaje': ((i + 1) / total) * 90}
                        file_write = open(self.archivo_log, 'w')
                        file_write.write(json.dumps(log))
                        file_write.close()
                    if functions.current_time(as_string=False) - tiempo > 15:
                        respuesta['inicio'] = i
                        break

                zip.close()
                if 'inicio' not in respuesta:
                    my_file = Path(self.base_dir + '/bdd.sql')
                    if my_file.is_file():
                        log = {'mensaje': 'Restaurando Base de datos',
                               'porcentaje': 95}
                        file_write = open(self.archivo_log, 'w')
                        file_write.write(json.dumps(log))
                        file_write.close()
                        connection = database.instance()
                        exito = connection.restore_backup(
                            self.base_dir + '/bdd.sql')
                        if not isinstance(exito, bool) or not exito:
                            respuesta['errores'].append(exito)

                    else:
                        respuesta['mensaje'] = 'No existe base de datos'
                        respuesta['errores'].append('bdd.sql')
                respuesta['exito'] = True
            else:
                respuesta['mensaje'] = 'Error al abrir archivo, o archivo no valido'

        if 'inicio' not in respuesta:
            c = configuracion_administrador()
            c.json_update(False)

            log = {'mensaje': 'Restauracion finalizada', 'porcentaje': 100}
            file_write = open(self.archivo_log, 'w')
            file_write.write(json.dumps(log))
            file_write.close()
        ret['body'] = json.dumps(respuesta)
        return ret

    def eliminar(self):
        ret = {'body': ''}
        campos = app.post['campos']
        respuesta = {'exito': False, 'mensaje': ''}
        id = campos['id']

        file = []
        for root, dirs, files in os.walk(self.dir_backup):
            for fichero in files:
                if id in fichero:
                    file.append(fichero)

        file = file.pop()

        if os.access(self.dir_backup + '/' + file, os.W_OK) is not True:
            respuesta['mensaje'] = 'Debes dar permisos de escritura o eliminar el archivo manualmente'
        else:
            os.remove(self.dir_backup + '/' + file)
            respuesta['exito'] = True
            respuesta['mensaje'] = "Eliminado correctamente."

        ret['body'] = json.dumps(respuesta)
        return ret

    def vaciar_log(self):
        ret = {'body': ''}
        my_file = Path(self.archivo_log)
        if my_file.is_file():
            os.remove(self.archivo_log)
        ret['body'] = "'True'"
        return ret

    def actualizar_tiempo(self):
        '''actualiza el tiempo total del respaldo realizado, para dar informacion del tiempo promedio de respaldo'''
        ret = {'body': ''}
        respuesta = {'exito': False}
        campos = app.post
        if 'tiempo' in campos and 'tipo_backup' in campos:
            cantidad = configuracion_model.getByVariable(
                'cantidad_backup_' + campos['tipo_backup'])
            if isinstance(cantidad, bool):
                cantidad = 0
            else:
                cantidad = float(cantidad)

            tiempo = configuracion_model.getByVariable(
                'tiempo_backup_' + campos['tipo_backup'])
            if isinstance(tiempo, bool):
                tiempo = 0
            else:
                tiempo = float(tiempo)

            tiempo = (tiempo * cantidad) + float(campos['tiempo'])
            cantidad += 1
            tiempo = tiempo / cantidad
            configuracion_model.setByVariable(
                'cantidad_backup_' + campos['tipo_backup'], cantidad)
            configuracion_model.setByVariable(
                'tiempo_backup_' + campos['tipo_backup'], tiempo)
            respuesta['exito'] = True
            respuesta['mensaje'] = 'tiempo: ' + \
                str(tiempo) + ', cantidad: ' + str(cantidad)

        ret['body'] = json.dumps(respuesta)
        return ret

    def eliminar_error(self):
        '''Elimina archivos que no se lograron completar'''
        ret = {'body': ''}
        respuesta = {'exito': True}

        files = []
        for root, dirs, file in os.walk(self.dir_backup):
            for fichero in file:
                name, extension = os.path.splitext(fichero)
                if(extension != '.zip'):
                    files.append(name+extension)

        url = app.get_dir(True) + 'backup/'

        for f in files:
            os.remove(url + f)
        ret['body'] = json.dumps(respuesta)
        return ret

    def generar(self):
        '''comprueba las carpetas de respaldo y obtiene la lista de archivos para respaldar en zip'''
        ret = {'body': ''}
        c = configuracion_administrador()
        c.json(False)
        respuesta = {'exito': True, 'mensaje': ''}

        my_file = Path(self.dir_backup)
        if my_file.is_dir():
            if os.access(self.dir_backup, os.W_OK) is not True:
                respuesta['mensaje'] = 'Debes dar permisos de escritura o eliminar el archivo ' + self.dir_backup
                respuesta['exito'] = False

        elif os.access(self.base_dir, os.W_OK) is not True:
            respuesta['mensaje'] = 'Debes dar permisos de escritura en ' + self.base_dir
            respuesta['exito'] = False

        if respuesta['exito']:
            respuesta = self.get_files(self, self.base_dir)

        ret['body'] = json.dumps(respuesta)
        return ret

    def generar_backup(self, log=True):
        '''genera respaldo del sitio en zip, en formato "Respaldo rapido" (usa mas recursos)'''
        ret = {'body': ''}
        c = configuracion_administrador()
        c.json(False)
        respuesta = {'exito': True, 'mensaje': ''}

        my_file = Path(self.dir_backup)
        if my_file.is_dir():
            if os.access(self.dir_backup, os.W_OK) is not True:
                respuesta['mensaje'] = 'Debes dar permisos de escritura o eliminar el archivo ' + self.dir_backup
                respuesta['exito'] = False

        elif os.access(self.base_dir, os.W_OK) is not True:
            respuesta['mensaje'] = 'Debes dar permisos de escritura en ' + self.base_dir
            respuesta['exito'] = False

        if respuesta['exito']:
            respuesta = self.get_files(self, self.base_dir)

        if respuesta['exito']:
            total = len(respuesta['lista'])
            if respuesta['lista'] > 0:
                respuesta['exito'] = True
                while len(respuesta['lista']) > 0 and respuesta['exito']:
                    respuesta = self.zipData(
                        self.base_dir, respuesta['archivo_backup'], respuesta['lista'], total, log)

        if respuesta['exito']:
            if log:
                log = {'mensaje': 'Respaldando Base de datos ', 'porcentaje': 90}
                file_write = open(self.archivo_log, 'w')
                file_write.write(json.dumps(log))
                file_write.close()
            respuesta = self.bdd(False, respuesta['archivo_backup'])

        if respuesta['exito']:
            if log:
                log = {'mensaje': 'Restauracion finalizada', 'porcentaje': 100}
                file_write = open(self.archivo_log, 'w')
                file_write.write(json.dumps(log))
                file_write.close()

        if log:
            ret['body'] = json.dumps(respuesta)
            return ret
        else:
            return respuesta

    def get_files(self, source: str, log=True):
        '''obtiene lista de archivos para respaldar en zip'''
        respuesta = {'exito': False,
                     'mensaje': 'Debes instalar la extension ZIP'}
        my_file = Path(source)
        if my_file.is_dir():
            lista_archivos = []
            count = 0
            for root, dirs, file in os.walk(source):
                for fichero in file:
                    if '.git' not in root and '.zip' not in fichero and '.sql' not in fichero and fichero != '.' and fichero != '..' and fichero[-1:] != '.' and fichero[-2:] != '..':
                        count += 1
                        print('root:',root,'fichero:',fichero)
                        fichero_final=root+fichero
                        fichero_final = fichero_final.replace("\\", "/")
                        lista_archivos.append(fichero_final)

                        if log and count % 1000 == 0:
                            log_file = {
                                'mensaje': 'Recuperando archivo ' + fichero, 'porcentaje': 10
                            }
                            file_write = open(self.archivo_log, 'w+')
                            file_write.write(json.dumps(log_file))
                            file_write.close()
            print(lista_archivos)
            respuesta['lista'] = lista_archivos
            respuesta['archivo_backup'] = self.dir_backup + '/' + app.prefix_site + \
                '-' + str(functions.current_time(as_string=False)) + '.zip'
            respuesta['exito'] = True
        else:
            respuesta['mensaje'] = 'Directorio no valido'

        return respuesta

    def bdd(self, log=True, archivo_backup=''):
        '''crea respaldo de la base de datos y la agrega al archivo zip'''
        import zipfile
        ret = {'body': ''}
        if archivo_backup == '':
            archivo_backup = app.post['archivo_backup']

        connection = database.instance()
        respuesta = connection.backup()
        if respuesta['exito']:
            try:
                zip = zipfile.ZipFile(archivo_backup, 'w')
                zip.writestr('bdd.sql', "\n".join(respuesta['sql']))
                zip.close()
            except:
                respuesta['exito'] = False
                respuesta['mensaje'] = 'Ocurrio un error al intentar guardar la base de datos en archivo zip ' + archivo_backup
        if log:
            ret['body'] = json.dumps(respuesta)
            return ret
        else:
            return respuesta

    def continuar(self):
        '''Inicio o continuacion de respaldo en modo lento (toma mas tiempo pero consume menos recursos)'''
        ret = {'body': ''}
        lista=json.loads(app.post['lista'])
        respuesta = self.zipData(self.base_dir, app.post['archivo_backup'], lista, app.post['total'])
        ret['body'] = json.dumps(respuesta)
        return ret

    def zipData(self, source, destination, lista, total=1, log=True):
        '''recorre los archivos entregados y crea un archivo zip'''
        import zipfile
        respuesta = {'exito': False, 'mensaje': 'Error al crear archivo'}
        tiempo = 0
        archivo = destination

        memory_limit = 128*1024*1024
        memory_limit = (int)(memory_limit) / 1.5
        memory_usage = 0

        zip = zipfile.ZipFile(archivo, 'w')
        count = 0
        for file in lista:
            count += 1
            memory_usage += os.path.getsize(source + '/' + file)
            if memory_usage > memory_limit:
                break

            my_file = Path(source + '/' + file)
            if my_file.is_dir():
                zip.writestr(zipfile.ZipInfo(source + '/' + file), '')
            else:
                zip.write(source + '/' + file)

            del file

            if log and (functions.current_time(as_string=False) - tiempo > 5 or count % 1000 == 0):
                log_file = {
                    'mensaje': file[-30:] + ' (' + str(total - len(lista)) + '/' + str(total) + ')',
                    'porcentaje': 10 + ((total - len(lista)) / total) * 40
                }
                file_write = open(self.archivo_log, 'w')
                file_write.write(json.dumps(log_file))
                file_write.close()
                tiempo = functions.current_time(as_string=False)

        if log:
            log_file = {
                'mensaje': file[-30:] + ' (' + str(total - len(lista)) + '/' + str(total) + ')',
                'notificacion': 'Guardando archivo, Esta operacion puede tomar algun tiempo',
                'porcentaje': 10 + ((total - len(lista)) / total) * 40
            }
            file_write = open(self.archivo_log, 'w')
            file_write.write(json.dumps(log_file))
            file_write.close()

        zip.close()
        respuesta['exito'] = True
        respuesta['lista'] = lista
        respuesta['archivo_backup'] = destination
        respuesta['archivo_actual'] = file

        return respuesta
