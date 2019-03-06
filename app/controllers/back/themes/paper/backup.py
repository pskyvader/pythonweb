from .base import base
from app.models.administrador import administrador as administrador_model

from core.app import app
from core.functions import functions

class backup(base):
    url = ['backup']
    metadata = {'title' : 'backup','modulo':'backup'}
    breadcrumb = []
    dir_base         = ''
    dir_backup  = ''
    archivo_log = ''
    no_restore   = ['backup/']
    
    def __init__(self):
        self.dir_base         = app.get_dir(True)
        self.dir_backup  = self.dir_base + 'backup'
        self.archivo_log = app.get_dir() + '/log.json'


    @classmethod
    def index(cls):
        '''Controlador de lista_class de elementos base, puede ser sobreescrito en el controlador de cada modulo'''
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

        # cabeceras y campos que se muestran en la lista_class:
        # titulo,campo de la tabla a usar, tipo (ver archivo lista_class.py funcion "field")
        # controlador de lista_class
        lista = lista_class(cls.metadata)
        configuracion = lista.configuracion(cls.metadata['modulo'])
        if 'error' in configuracion:
            ret['error']=configuracion['error']
            ret['redirect']=configuracion['redirect']
            return ret

        where = {}
        if cls.contiene_tipos:
            where['tipo'] = get['tipo']
        if cls.contiene_hijos:
            where['idpadre'] = get['idpadre']
        if cls.class_parent != None:
            class_parent = cls.class_parent

            if class_parent.idname in get:
                where[class_parent.idname] = get[class_parent.idname]

        condiciones = {}
        url_detalle = url_final.copy()
        url_detalle.append('detail')
        # obtener unicamente elementos de la pagina actual
        respuesta = lista.get_row(class_name, where, condiciones, url_detalle)

        if 'copy' in configuracion['th']:
            configuracion['th']['copy']['action'] = configuracion['th']['copy']['field']
            configuracion['th']['copy']['field'] = 0
            configuracion['th']['copy']['mensaje'] = 'Copiando'

        if cls.contiene_hijos:
            if cls.contiene_tipos:
                for v in respuesta['row']:
                    v['url_children'] = functions.generar_url(
                        url_final, {'idpadre': v[0], 'tipo': get['tipo']})

            else:
                for v in respuesta['row']:
                    v['url_children'] = functions.generar_url(
                        url_final, {'idpadre': v[0]})

        else:
            if 'url_children' in configuracion['th']:
                del configuracion['th']['url_children']

        if cls.sub != '':
            if cls.contiene_tipos:
                for v in respuesta['row']:
                    v['url_sub'] = functions.generar_url(
                        [cls.sub], {class_name.idname: v[0], 'tipo': get['tipo']})

            else:
                for v in respuesta['row']:
                    v['url_sub'] = functions.generar_url(
                        [cls.sub], {class_name.idname: v[0]})

        else:
            if 'url_sub' in configuracion['th']:
                del configuracion['th']['url_sub']

        # informacion para generar la vista de lista_class
        data = {
            'breadcrumb': cls.breadcrumb,
            'th': configuracion['th'],
            'current_url': functions.generar_url(url_final),
            'new_url': functions.generar_url(url_detalle),
        }

        data.update(respuesta)
        data.update(configuracion['menu'])
        ret = lista.normal(data)
        return ret
    




    public function index()
    {
        if (!administrador_model::verificar_sesion()) {
            $this->url = array('login', 'index', 'backup');
        }
        functions::url_redirect($this->url);

        $head = new head($this->metadata);
        $head->normal();

        $header = new header();
        $header->normal();
        $aside = new aside();
        $aside->normal();

        $mensaje_error = '';
        if (file_exists($this->dir_backup)) {
            if (!is_writable($this->dir_backup)) {
                $mensaje_error = 'Debes dar permisos de escritura o eliminar el archivo ' . $this->dir_backup;
            }
        } elseif (!is_writable($this->dir)) {
            $mensaje_error = 'Debes dar permisos de escritura en ' . $this->dir;
        }
        $is_error = ($mensaje_error != '');

        $is_mensaje = false;

        $mensaje      = "Tiempo promedio de respaldo: ";
        $tiempo_lento = configuracion_model::getByVariable('tiempo_backup_lento');
        if (is_bool($tiempo_lento)) {
            $tiempo_lento = 0;
        } else {
            $tiempo_lento = (int) $tiempo_lento;
            $is_mensaje   = true;
            $mensaje .= $tiempo_lento . " segundos (servidor lento)";
        }
        $tiempo_rapido = configuracion_model::getByVariable('tiempo_backup_rapido');
        if (is_bool($tiempo_rapido)) {
            $tiempo_rapido = 0;
        } else {
            $tiempo_rapido = (int) $tiempo_rapido;
            $is_mensaje    = true;
            if ($tiempo_lento > 0) {
                $mensaje .= ", ";
            }
            $mensaje .= $tiempo_rapido . " segundos (servidor rápido)";
        }

        $row   = array();
        $files = array_filter(scandir($this->dir_backup), function ($item) {
            if (is_file($this->dir_backup . '/' . $item)) {
                $extension = explode('.', $item);
                $extension = array_pop($extension);
                if ($extension == 'zip') {
                    return true;
                }
            }
            return false;
        });
        $url = app::get_url(true) . 'backup/';

        foreach ($files as $key => $f) {
            $extension = explode('.', $f);
            array_pop($extension);
            $fecha       = explode('-', implode('.', $extension));
            $fecha       = array_pop($fecha);
            $row[$fecha] = array(
                'even'  => ($key % 2 == 0),
                'id'    => $fecha,
                'fecha' => functions::formato_fecha($fecha),
                'size'  => functions::file_size($this->dir_backup . '/' . $f),
                'url'   => $url . $f,
            );
        }
        $row = array_reverse($row);

        view::set('row', $row);
        view::set('breadcrumb', $this->breadcrumb);
        view::set('title', $this->metadata['title']);
        view::set('is_error', $is_error);
        view::set('mensaje_error', $mensaje_error);
        view::set('is_mensaje', $is_mensaje);
        view::set('mensaje', $mensaje);
        view::set('tiempo_lento', $tiempo_lento);
        view::set('tiempo_rapido', $tiempo_rapido);
        view::render('backup');

        $footer = new footer();
        $footer->normal();
    }