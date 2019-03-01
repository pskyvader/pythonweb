from app.models.moduloconfiguracion import moduloconfiguracion as moduloconfiguracion_model

class base:
    url            = []
    metadata       = {}
    class_name          = None
    breadcrumb     = []
    contiene_tipos = False
    contiene_hijos = False

    def __init__(self, class_name):
        moduloconfiguracion = moduloconfiguracion_model.getByModulo(base.metadata['modulo'])
        if 0 in moduloconfiguracion:
            base.contiene_tipos = (isset(moduloconfiguracion['tipos'])) ? moduloconfiguracion['tipos'] : false
            base.sub            = (isset(moduloconfiguracion['sub'])) ? moduloconfiguracion['sub'] : ''
            base.padre          = (isset(moduloconfiguracion['padre'])) ? moduloconfiguracion['padre'] : ''
            if (base.contiene_tipos && isset(_GET['tipo'])) {
                tipo = _GET['tipo']
            } else {
                tipo = 0
            }


            modulo                  = modulo_model.getAll(array('idmoduloconfiguracion' => moduloconfiguracion[0], 'tipo' => tipo))
            base.contiene_hijos    = (isset(modulo[0]['hijos'])) ? modulo[0]['hijos'] : false
            base.metadata['title'] = modulo[0]['titulo']
            
            if (base.padre != '') {
                parent             = '\app\models\\' . base.padre
                base.class_parent = new parent()
                if (isset(_GET[base.class_parent.idname])) {
                    p=base.class_parent.getById(_GET[base.class_parent.idname])
                    if(count(p>0)){
                        if(isset(p['titulo']) && p['titulo']!=''){
                            base.metadata['title'].=' - '.p['titulo']
                        }elseif(isset(p['nombre']) && p['nombre']!=''){
                            base.metadata['title'].=' - '.p['nombre']
                        }
                    }

                }
            }
        }

        base.class_name      = class_name
        base.breadcrumb = array(
            array('url' => functions.generar_url(array("home")), 'title' => 'Home', 'active' => ''),
            array('url' => functions.generar_url(base.url), 'title' => (base.metadata['title']), 'active' => 'active'),
        )
    }




class base
{
    protected $url            = array();
    protected $metadata       = array();
    protected $class          = null;
    protected $breadcrumb     = array();
    protected $contiene_tipos = false;
    protected $contiene_hijos = false;
    
    public function index()
    {
        $class = $this->class; // Clase para enviar a controlador de lista
        if ($this->contiene_tipos && !isset($_GET['tipo'])) {
            $this->url = array('home');
        }
        if ($this->contiene_hijos && !isset($_GET['idpadre'])) {
            $this->url = array('home');
        }

        if (!administrador_model.verificar_sesion()) {
            $this->url = array_merge(array('login', 'index'), $this->url);
        }
        functions.url_redirect($this->url); //verificar sesion o redireccionar a login

        /* cabeceras y campos que se muestran en la lista:
        titulo,campo de la tabla a usar, tipo (ver archivo lista.php funcion "field") */

        $list          = new lista($this->metadata); //controlador de lista
        $configuracion = $list->configuracion($this->metadata['modulo']);

        $where = array();
        if ($this->contiene_tipos) {
            $where['tipo'] = $_GET['tipo'];
        }
        if ($this->contiene_hijos) {
            $where['idpadre'] = $_GET['idpadre'];
        }
        if (isset($this->class_parent)) {
            $class_parent = $this->class_parent;

            if (isset($_GET[$class_parent.$idname])) {
                $where[$class_parent.$idname] = $_GET[$class_parent.$idname];
            }
        }
        $condiciones   = array();
        $url_detalle   = $this->url;
        $url_detalle[] = 'detail';
        $respuesta     = $list->get_row($class, $where, $condiciones, $url_detalle); //obtener unicamente elementos de la pagina actual

        if (isset($configuracion['th']['copy'])) {
            $configuracion['th']['copy']['action']  = $configuracion['th']['copy']['field'];
            $configuracion['th']['copy']['field']   = 0;
            $configuracion['th']['copy']['mensaje'] = 'Copiando';
        }

        if ($this->contiene_hijos) {
            if ($this->contiene_tipos) {
                foreach ($respuesta['row'] as $k => $v) {
                    $respuesta['row'][$k]['url_children'] = functions.generar_url($this->url, array('idpadre' => $v[0], 'tipo' => $_GET['tipo']));
                }
            } else {
                foreach ($respuesta['row'] as $k => $v) {
                    $respuesta['row'][$k]['url_children'] = functions.generar_url($this->url, array('idpadre' => $v[0]));
                }
            }
        } else {
            unset($configuracion['th']['url_children']);
        }

        if ($this->sub != '') {
            if ($this->contiene_tipos) {
                foreach ($respuesta['row'] as $k => $v) {
                    $respuesta['row'][$k]['url_sub'] = functions.generar_url(array($this->sub), array($class.$idname => $v[0], 'tipo' => $_GET['tipo']));
                }
            } else {
                foreach ($respuesta['row'] as $k => $v) {
                    $respuesta['row'][$k]['url_sub'] = functions.generar_url(array($this->sub), array($class.$idname => $v[0]));
                }
            }
        } else {
            unset($configuracion['th']['url_sub']);
        }

        $data = array( //informacion para generar la vista de la lista, arrays SIEMPRE antes de otras variables!!!!
            'breadcrumb'  => $this->breadcrumb,
            'th'          => $configuracion['th'],
            'current_url' => functions.generar_url($this->url),
            'new_url'     => functions.generar_url($url_detalle),
        );
        $data = array_merge($data, $respuesta, $configuracion['menu']);

        $list->normal($data);
    }

    public function detail($var = array())
    {
        $class       = $this->class; // Clase para enviar a controlador de detalle
        $url_save    = $url_list    = $this->url;
        $url_save[]  = 'guardar';
        $this->url[] = 'detail';
        if (isset($var[0])) {
            $id                      = (int) $var[0];
            $this->url[]             = $id;
            $this->metadata['title'] = 'Editar ' . $this->metadata['title'];
        } else {
            $id                      = 0;
            $this->metadata['title'] = 'Nuevo ' . $this->metadata['title'];
        }

        $this->breadcrumb[] = array('url' => functions.generar_url($this->url), 'title' => ($this->metadata['title']), 'active' => 'active');
        if ($this->contiene_tipos && !isset($_GET['tipo'])) {
            $this->url = array('home');
        }
        if (!administrador_model.verificar_sesion()) {
            $this->url = array_merge(array('login', 'index'), $this->url);
        }
        functions.url_redirect($this->url); //verificar sesion o redireccionar a login

        /* cabeceras y campos que se muestran en el detalle:
        titulo,campo de la tabla a usar, tipo (ver archivo detalle.php funcion "field") */

        $detalle       = new detalle($this->metadata); //controlador de detalle
        $configuracion = $detalle->configuracion($this->metadata['modulo']);
        $row           = ($id != 0) ? ($class.getById($id)) : array();
        if ($this->contiene_tipos) {
            $configuracion['campos']['tipo'] = array('title_field' => 'tipo', 'field' => 'tipo', 'type' => 'hidden', 'required' => true);
            $row['tipo']                     = $_GET['tipo'];
        }
        if ($this->contiene_hijos && isset($configuracion['campos']['idpadre'])) {
            $categorias = $class.getAll();
            foreach ($categorias as $key => $c) {
                if ($c[0] == $id) {
                    unset($categorias[$key]);
                    break;
                }
            }
            $raiz = array(0, 'titulo' => 'Raíz', 'idpadre' => array(-1));
            array_unshift($categorias, $raiz);
            $configuracion['campos']['idpadre']['parent'] = functions.crear_arbol($categorias, -1);
        } else if ($this->contiene_hijos || isset($configuracion['campos']['idpadre'])) {
            $configuracion['campos']['idpadre'] = array('title_field' => 'idpadre', 'field' => 'idpadre', 'type' => 'hidden', 'required' => true);
            if ($id == 0) {
                if (isset($_GET['idpadre'])) {
                    $row['idpadre'] = functions.encode_json(array((string) $_GET['idpadre']));
                } else {
                    $row['idpadre'] = functions.encode_json(array('0'));
                }
            }
        } else {
            unset($configuracion['campos']['idpadre']);
        }

        if (isset($this->class_parent)) {
            $class_parent = $this->class_parent;
            $idparent     = $class_parent.$idname;

            $is_array = true;
            $fields   = table.getByname($class.$table);
            if (isset($fields[$idparent]) && $fields[$idparent]['tipo'] != 'longtext') {
                $is_array = false;
            }
            if (isset($configuracion['campos'][$idparent])) {
                $categorias = $class_parent.getAll();
                if ($is_array) {
                    $configuracion['campos'][$idparent]['parent'] = functions.crear_arbol($categorias);
                } else {
                    $configuracion['campos'][$idparent]['parent'] = $categorias;
                }
            } else {
                $configuracion['campos'][$idparent] = array('title_field' => $idparent, 'field' => $idparent, 'type' => 'hidden', 'required' => true);
                if ($id == 0) {
                    if (isset($_GET[$idparent])) {
                        if ($is_array) {
                            $row[$idparent] = functions.encode_json(array((string) $_GET[$idparent]));
                        } else {
                            $row[$idparent] = (int) $_GET[$idparent];
                        }

                    } else {
                        if ($is_array) {
                            $row[$idparent] = functions.encode_json(array('0'));
                        } else {
                            $row[$idparent] = 0;
                        }
                    }
                } else {
                    if ($is_array) {
                        $row[$idparent] = functions.encode_json($row[$idparent]);
                    } else {
                        $row[$idparent] = $row[$idparent];
                    }
                }
            }
        }

        $data = array( //informacion para generar la vista del detalle, arrays SIEMPRE antes de otras variables!!!!
            'breadcrumb'  => $this->breadcrumb,
            'campos'      => $configuracion['campos'],
            'row'         => $row,
            'id'          => ($id != 0) ? $id : '',
            'current_url' => functions.generar_url($this->url),
            'save_url'    => functions.generar_url($url_save),
            'list_url'    => functions.generar_url($url_list),
        );

        $detalle->normal($data, $class);
    }

    public function orden()
    {
        $respuesta = lista.orden($this->class);
        echo json_encode($respuesta);
    }

    public function estado()
    {
        $respuesta = lista.estado($this->class);
        echo json_encode($respuesta);
    }
    public function eliminar()
    {
        $respuesta = lista.eliminar($this->class);
        echo json_encode($respuesta);
    }
    public function copy()
    {
        $respuesta = lista.copy($this->class);
        echo json_encode($respuesta);
    }
    public function excel()
    {
        $respuesta = array('exito' => false, 'mensaje' => 'Debes recargar la pagina');
        if ($this->contiene_tipos && !isset($_GET['tipo'])) {
            echo json_encode($respuesta);
            return;
        }
        if ($this->contiene_hijos && !isset($_GET['idpadre'])) {
            echo json_encode($respuesta);
            return;
        }
        $where = array();
        if ($this->contiene_tipos) {
            $where['tipo'] = $_GET['tipo'];
        }
        if ($this->contiene_hijos) {
            $where['idpadre'] = $_GET['idpadre'];
        }
        if (isset($this->class_parent)) {
            $class_parent = $this->class_parent;
            if (isset($_GET[$class_parent.$idname])) {
                $where[$class_parent.$idname] = $_GET[$class_parent.$idname];
            }
        }
        $select    = "";
        $respuesta = lista.excel($this->class, $where, $select, $this->metadata['title']);
        echo json_encode($respuesta);
    }

    public function get_all()
    {
        $respuesta = array('exito' => false, 'mensaje' => 'Debes recargar la pagina');
        if ($this->contiene_tipos && !isset($_GET['tipo'])) {
            echo json_encode($respuesta);
            return;
        }
        if ($this->contiene_hijos && !isset($_GET['idpadre'])) {
            echo json_encode($respuesta);
            return;
        }
        $where = array();
        if ($this->contiene_tipos) {
            $where['tipo'] = $_GET['tipo'];
        }
        if ($this->contiene_hijos) {
            $where['idpadre'] = $_GET['idpadre'];
        }
        if (isset($this->class_parent)) {
            $class_parent = $this->class_parent;
            if (isset($_GET[$class_parent.$idname])) {
                $where[$class_parent.$idname] = $_GET[$class_parent.$idname];
            }
        }
        $condiciones = array();
        $select      = "";
        $class       = $this->class;
        $row         = $class.getAll($where, $condiciones, $select);
        echo json_encode($row);
    }

    public function regenerar()
    {
        $respuesta = image.regenerar($_POST);
        echo json_encode($respuesta);
    }

    public function guardar()
    {
        $respuesta = detalle.guardar($this->class);
        echo json_encode($respuesta);
    }

    public function upload()
    {
        $respuesta = image.upload_tmp($this->metadata['modulo']);
        echo json_encode($respuesta);
    }

    public function upload_file()
    {
        $respuesta = file.upload_tmp();
        echo json_encode($respuesta);
    }
}
