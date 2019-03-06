from .base import base
from app.models.administrador import administrador as administrador_model
from app.models.configuracion import configuracion as configuracion_model


from .head import head
from .header import header
from .aside import aside
from .footer import footer

from core.app import app
from core.functions import functions
from core.view import view

from pathlib import Path

class backup(base):
    url = ['backup']
    metadata = {'title' : 'backup','modulo':'backup'}
    breadcrumb = []
    base_dir         = ''
    dir_backup  = ''
    archivo_log = ''
    no_restore   = ['backup/']
    
    def __init__(self):
        self.base_dir         = app.get_dir(True)
        self.dir_backup  = self.base_dir + 'backup'
        self.archivo_log = app.get_dir() + '/log.json'


    @classmethod
    def index(cls):
        '''Controlador de lista_class de elementos base, puede ser sobreescrito en el controlador de cada modulo'''
        import os
        ret = {'body': ''}
        # Clase para enviar a controlador de lista_class
        url_final=cls.url.copy()
        get = app.get
        
        if not administrador_model.verificar_sesion():
            url_final = ['login', 'index'] + url_final
        # verificar sesion o redireccionar a login
        url_return = functions.url_redirect(url_final)
        if url_return != '':
            ret['error'] = 301
            ret['redirect'] = url_return
            return ret

        h = head(cls.metadata)
        ret_head=h.normal()
        if ret_head['headers']!='':
            return ret_head
        ret['body']+=ret_head['body']
        
        he=header()
        ret['body']+=he.normal()['body']

        asi = aside()
        ret['body']+=asi.normal()['body']




        mensaje_error = ''
        my_file = Path(cls.dir_backup)
        if my_file.is_dir():
            if os.access(cls.dir_backup, os.W_OK) is not True:
                mensaje_error = 'Debes dar permisos de escritura o eliminar el archivo ' + cls.dir_backup
            
        elif os.access(cls.base_dir, os.W_OK) is not True:
            mensaje_error = 'Debes dar permisos de escritura en ' + cls.base_dir
        
        is_error = (mensaje_error != '')

        is_mensaje = False

        mensaje      = "Tiempo promedio de respaldo: "
        tiempo_lento = configuracion_model.getByVariable('tiempo_backup_lento')
        if isinstance(tiempo_lento,bool):
            tiempo_lento = 0
        else:
            tiempo_lento = int(tiempo_lento)
            is_mensaje   = True
            mensaje += tiempo_lento + " segundos (servidor lento)"
        
        tiempo_rapido = configuracion_model.getByVariable('tiempo_backup_rapido')
        if isinstance(tiempo_rapido,bool):
            tiempo_rapido = 0
        else:
            tiempo_rapido = int(tiempo_rapido)
            is_mensaje    = True
            if tiempo_lento > 0:
                mensaje += ", "
            
            mensaje += tiempo_rapido + " segundos (servidor rápido)"
        

        row   = {}
        files=[]
        for root, dirs, file in os.walk(cls.dir_backup):
            for fichero in file:
                name, extension = os.path.splitext(fichero)
                if(extension == ".zip"):
                    files.append(name+extension)

        url = app.get_url(True) + 'backup/'

        for key,f in dict.fromkeys(files):
            name, extension = os.path.splitext(f)
            fecha       = name.split('-')
            fecha       = fecha.pop()
            row[fecha] = {
                'even'  : (key % 2 == 0),
                'id'    : fecha,
                'fecha' : functions.formato_fecha(fecha),
                'size'  : functions.file_size(cls.dir_backup + '/' + f),
                'url'   : url + f,
            }

        view.add('row', row)
        view.add('breadcrumb', cls.breadcrumb)
        view.add('title', cls.metadata['title'])
        view.add('is_error', is_error)
        view.add('mensaje_error', mensaje_error)
        view.add('is_mensaje', is_mensaje)
        view.add('mensaje', mensaje)
        view.add('tiempo_lento', tiempo_lento)
        view.add('tiempo_rapido', tiempo_rapido)
        ret['body']+=view.render('backup')

        
        f = footer()
        ret['body']+=f.normal()['body']    
        return ret
    
