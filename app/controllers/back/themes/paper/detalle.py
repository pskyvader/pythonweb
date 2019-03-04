from core.app import app
from core.view import view
from .head import head
from .header import header
from .aside import aside
from .footer import footer

class detalle:
    metadata   = {'title' : ''}
    max_upload = "Ilimitado"

    def __init__(self,metadata):
        for key, value in metadata.items():
            self.metadata[key] = value

    def normal(self, data: dict):
        ret = {'body': ''}
        campos = data['campos']
        row_data = data['row']
        row = []

        for v in campos:
            content = self.field(v, row_data)
            row.append({'content' : content, 'content_field' : v['field'], 'class' : 'hidden' if 'hidden' == v['type'] else ''})

        data['row'] = row
        data['title'] = self.metadata['title']

        h = head(self.metadata)
        ret_head = h.normal()
        if ret_head['headers'] != '':
            return ret_head
        ret['body'] += ret_head['body']

        he = header()
        ret['body'] += he.normal()['body']

        asi = aside()
        ret['body'] += asi.normal()['body']

        view.add_array(data)
        view.render('detail')

        f = footer()
        ret['body'] += f.normal()['body']

    @staticmethod
    def configuracion(modulo, force = False):
        tipo_admin          = app.session["tipo" + app.prefix_site]
        moduloconfiguracion = moduloconfiguracion_model.getByModulo(modulo)
        var                 = {'idmoduloconfiguracion' : moduloconfiguracion[0]}
        if 'tipo' in app.get:
            var['tipo'] = app.get['tipo']
        
        modulo  = modulo_model.getAll(var, {'limit' : 1})
        modulo  = modulo[0]
        estados = modulo['estado'][0]['estado']
        if 'true' != estados[tipo_admin] and not force:
            return {'error': 301, 'redirect': functions.url_redirect(['home'])}
        
        campos = array()
        foreach (modulo['detalle'] as key : m:
            if 'true' == m['estado'][tipo_admin]:
                campos[m['field']] = array('title_field' : m['titulo'], 'field' : m['field'], 'type' : m['tipo'], 'required' : ('true' == m['required']) ? true : False, 'help' : m['texto_ayuda'])
            }
        }

        return array('campos' : campos)




        
    private function field($campos, $fila, $parent = '', $idparent = 0, $level = 0)
    {
        $editor_count = 0;
        switch ($campos['type']:
            case 'active':
                $data = array(
                    'title_field' : $campos['title_field'],
                    'field'       : $campos['field'],
                    'is_required' : $campos['required'],
                    'required'    : ($campos['required']) ? 'required="required"' : '',
                    'active'      : (isset($fila[$campos['field']])) ? (string) $fila[$campos['field']] : '',
                    'class'       : (isset($fila[$campos['field']])) ? (($fila[$campos['field']]) ? 'btn-success' : 'btn-danger') : 'btn-default',
                    'icon'        : (isset($fila[$campos['field']])) ? (($fila[$campos['field']]) ? 'fa-check' : 'fa-close') : 'fa-question-circle',
                );
                break;
            case 'color':
                $data = array(
                    'title_field' : $campos['title_field'],
                    'field'       : $campos['field'],
                    'is_required' : $campos['required'],
                    'required'    : ($campos['required']) ? 'required="required"' : '',
                    'value'       : (isset($fila[$campos['field']])) ? $fila[$campos['field']] : '',
                    'help'        : (isset($campos['help'])) ? $campos['help'] : '',
                );
                break;
            case 'date':
                $data = array(
                    'title_field' : $campos['title_field'],
                    'field'       : $campos['field'],
                    'is_required' : $campos['required'],
                    'required'    : ($campos['required']) ? 'required="required"' : '',
                    'help'        : (isset($campos['help'])) ? $campos['help'] : '',
                    'value'       : (isset($fila[$campos['field']])) ? $fila[$campos['field']] : '',
                );
                break;
            case 'daterange':
                $data = array(
                    'title_field' : $campos['title_field'],
                    'field'       : $campos['field'],
                    'is_required' : $campos['required'],
                    'required'    : ($campos['required']) ? 'required="required"' : '',
                    'help'        : (isset($campos['help'])) ? $campos['help'] : '',
                    'value'       : (isset($fila[$campos['field']])) ? $fila[$campos['field']] : '',
                );
                break;
            case 'editor':
                $data = array(
                    'title_field' : $campos['title_field'],
                    'field'       : $campos['field'],
                    'is_required' : $campos['required'],
                    'required'    : ($campos['required']) ? 'required="required"' : '',
                    'help'        : (isset($campos['help'])) ? $campos['help'] : '',
                    'value'       : (isset($fila[$campos['field']])) ? $fila[$campos['field']] : '',
                );
                $data['help'] .= " (Tamaño máximo de archivo " . $this->max_upload . ")";
                if 0 == $editor_count:
                    $theme           = app.get_url() . view.get_theme() . 'assets/ckeditor/';
                    $t               = '?t=I8BG';
                    $data['preload'] = array(
                        array('url' : 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css', 'type' : 'style'),
                        array('url' : 'https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css', 'type' : 'style'),
                        array('url' : 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js', 'type' : 'script'),
                        array('url' : 'https://code.jquery.com/jquery-1.11.3.min.js', 'type' : 'script'),

                        array('url' : $theme . 'contents.css', 'type' : 'style'),
                        array('url' : $theme . 'plugins/btgrid/styles/editor.css', 'type' : 'style'),
                        array('url' : $theme . 'plugins/tableselection/styles/tableselection.css', 'type' : 'style'),
                        array('url' : $theme . 'plugins/balloontoolbar/skins/default.css', 'type' : 'style'),
                        array('url' : $theme . 'plugins/balloontoolbar/skins/moono-lisa/balloontoolbar.css', 'type' : 'style'),
                        array('url' : $theme . 'plugins/balloonpanel/skins/moono-lisa/balloonpanel.css', 'type' : 'style'),

                        array('url' : $theme . 'skins/moono-lisa/editor.css' . $t, 'type' : 'style'),
                        array('url' : $theme . 'plugins/basewidget/css/style.css' . $t, 'type' : 'style'),
                        array('url' : $theme . 'plugins/layoutmanager/css/style.css' . $t, 'type' : 'style'),

                    );

                } else {
                    $data['preload'] = array();
                }
                $editor_count++;
                break;
            case 'grupo_pedido':
                $folder      = $this->metadata['modulo'];
                $direcciones = array();
                if isset($fila[$campos['field']]):
                    $count = count($fila[$campos['field']]);
                    foreach ($fila[$campos['field']] as $key : $campo:
                        $field                = $campo;
                        $field['title_field'] = $campos['title_field'];
                        $field['field']       = $campos['field'];
                        $direcciones[]        = $field;
                    }
                } else {
                    $count = 0;
                }
                foreach ($direcciones as $key : $d:
                    $direcciones[$key]['lista_productos']   = $campos['lista_productos'];
                    $direcciones[$key]['direccion_entrega'] = $campos['direccion_entrega'];
                    foreach ($direcciones[$key]['direccion_entrega'] as $k : $e:
                        if $e['idusuariodireccion'] == $d['idusuariodireccion']:
                            $direcciones[$key]['direccion_entrega'][$k]['selected'] = 'selected=""';
                        } else {
                            $direcciones[$key]['direccion_entrega'][$k]['selected'] = '';
                        }
                    }

                    foreach ($direcciones[$key]['productos'] as $k : $p:
                        $direcciones[$key]['productos'][$k]['lista_atributos'] = $campos['lista_atributos'];
                        foreach ($direcciones[$key]['productos'][$k]['lista_atributos'] as $f : $e:
                            if $e['idproducto'] == $p['idproductoatributo']:
                                $direcciones[$key]['productos'][$k]['lista_atributos'][$f]['selected'] = 'selected=""';
                            } else {
                                $direcciones[$key]['productos'][$k]['lista_atributos'][$f]['selected'] = '';
                            }
                        }
                    }

                }
                $data = array(
                    'title_field'       : $campos['title_field'],
                    'field'             : $campos['field'],
                    'is_required'       : $campos['required'],
                    'help'              : $campos['help'],
                    'required'          : ($campos['required']) ? 'required="required"' : '',
                    'direcciones'       : $direcciones,
                    'direccion_entrega' : $campos['direccion_entrega'],
                    'lista_productos'   : $campos['lista_productos'],
                    'lista_atributos'   : $campos['lista_atributos'],
                    'fecha'             : date('Y-m-d H:i:s'),
                    'count'             : ($count > 0) ? $count : '',
                );
                break;

            case 'multiple':
                $fields = array();
                $count  = (isset($fila[$campos['field']]) && is_array($fila[$campos['field']])) ? count($fila[$campos['field']]) : 0;
                if $count > 0:
                    foreach ($fila[$campos['field']] as $key : $f:
                        $td = array();
                        foreach ($campos['columnas'] as $k : $v:
                            $content = $this->field($v, $f, $campos['field'], $key);
                            $td[]    = array('content' : $content, 'content_field' : $v['field']);
                        }
                        $linea    = array('columna' : $td);
                        $fields[] = $linea;
                    }
                    $new_field = false;
                } else {
                    $new_field = true;
                }
                $new_line = array();
                foreach ($campos['columnas'] as $k : $v:
                    $content    = $this->field($v, array(), $campos['field']);
                    $new_line[] = array('content' : $content, 'content_field' : $v['field']);
                }

                $data = array(
                    'fields'      : $fields,
                    'count'       : $count,
                    'new_field'   : $new_field,
                    'new_line'    : $new_line,
                    'title_field' : $campos['title_field'],
                    'field'       : $campos['field'],
                    'is_required' : $campos['required'],
                    'required'    : ($campos['required']) ? 'required="required"' : '',
                );
                break;
            case 'multiple_text':
                $data = array(
                    'title_field' : $campos['title_field'],
                    'field'       : $campos['field'],
                    'parent'      : $parent,
                    'col'         : $campos['col'],
                    'is_required' : $campos['required'],
                    'required'    : ($campos['required']) ? 'required' : '',
                    'value'       : (isset($fila[$campos['field']])) ? $fila[$campos['field']] : '',
                );
                break;
            case 'multiple_number':
                $data = array(
                    'title_field' : $campos['title_field'],
                    'field'       : $campos['field'],
                    'parent'      : $parent,
                    'col'         : $campos['col'],
                    'max'         : $campos['max'],
                    'is_required' : $campos['required'],
                    'required'    : ($campos['required']) ? 'required' : '',
                    'value'       : (isset($fila[$campos['field']])) ? $fila[$campos['field']] : $campos['default'],
                );
                break;
            case 'multiple_label':
                $data = array(
                    'title_field' : $campos['title_field'],
                    'field'       : $campos['field'],
                    'parent'      : $parent,
                    'col'         : $campos['col'],
                    'is_required' : $campos['required'],
                    'required'    : ($campos['required']) ? 'required' : '',
                    'value'       : (isset($fila[$campos['field']])) ? $fila[$campos['field']] : '',
                );
                break;
            case 'multiple_hidden':
                $data = array(
                    'field'    : $campos['field'],
                    'parent'   : $parent,
                    'required' : ($campos['required']) ? 'required' : '',
                    'value'    : (isset($fila[$campos['field']])) ? $fila[$campos['field']] : '',
                );
                break;
            case 'multiple_select':
                foreach ($campos['option'] as $key : $option:
                    $campos['option'][$key]['selected'] = (isset($fila[$campos['field']]) && $fila[$campos['field']] == $option['value']) ? 'selected="selected"' : '';
                }
                $data = array(
                    'title_field' : $campos['title_field'],
                    'field'       : $campos['field'],
                    'parent'      : $parent,
                    'col'         : $campos['col'],
                    'option'      : $campos['option'],
                    'is_required' : $campos['required'],
                    'required'    : ($campos['required']) ? 'required' : '',
                );
                break;
            case 'multiple_button':
                $data = array(
                    'col' : $campos['col'],
                );
                break;
            case 'multiple_order':
                $data = array(
                    'col' : $campos['col'],
                );
                break;
            case 'multiple_active':
                $data = array(
                    'title_field' : $campos['title_field'],
                    'field'       : $campos['field'],
                    'parent'      : $parent,
                    'col'         : $campos['col'],
                    'is_required' : $campos['required'],
                    'required'    : ($campos['required']) ? 'required' : '',
                    'active'      : (isset($fila[$campos['field']])) ? (string) $fila[$campos['field']] : '',
                    'class'       : (isset($fila[$campos['field']])) ? (('true' == $fila[$campos['field']]) ? 'btn-success' : 'btn-danger') : 'btn-default',
                    'icon'        : (isset($fila[$campos['field']])) ? (('true' == $fila[$campos['field']]) ? 'fa-check' : 'fa-close') : 'fa-question-circle',
                );
                break;
            case 'multiple_active_array':
                $array = array();
                foreach ($campos['array'] as $key : $value:
                    $campos['array'][$key]['active'] = (isset($fila[$campos['field']][$key])) ? (string) $fila[$campos['field']][$key] : 'true';
                    $campos['array'][$key]['class']  = (isset($fila[$campos['field']][$key])) ? (('true' == $fila[$campos['field']][$key]) ? 'btn-success' : 'btn-danger') : 'btn-success';
                    $campos['array'][$key]['icon']   = (isset($fila[$campos['field']][$key])) ? (('true' == $fila[$campos['field']][$key]) ? 'fa-check' : 'fa-close') : 'fa-check';
                }
                $data = array(
                    'title_field' : $campos['title_field'],
                    'array'       : $campos['array'],
                    'field'       : $campos['field'],
                    'idparent'    : $idparent,
                    'parent'      : $parent,
                    'col'         : $campos['col'],
                    'is_required' : $campos['required'],
                    'required'    : ($campos['required']) ? 'required' : '',
                );
                break;
            case 'image':
                $folder    = $this->metadata['modulo'];
                $image_url = (isset($fila[$campos['field']]) && isset($fila[$campos['field']][0])) ? (image.generar_url($fila[$campos['field']][0], 'thumb')) : '';
                $data      = array(
                    'title_field'       : $campos['title_field'],
                    'field'             : $campos['field'],
                    'is_required'       : $campos['required'],
                    'is_required_modal' : ('' != $image_url) ? $campos['required'] : true,
                    'is_required_alert' : ('' != $image_url) ? $campos['required'] : true,
                    'required'          : ($campos['required']) ? 'required="required"' : '',
                    'image'             : $image_url,
                    'is_image'          : ('' != $image_url) ? true : false,
                    'url'               : ('' != $image_url) ? $fila[$campos['field']][0]['url'] : '',
                    'parent'            : ('' != $image_url) ? $fila[$campos['field']][0]['parent'] : '',
                    'folder'            : ('' != $image_url) ? $fila[$campos['field']][0]['folder'] : '',
                    'subfolder'         : ('' != $image_url) ? $fila[$campos['field']][0]['subfolder'] : '',
                    'help'              : (isset($campos['help'])) ? $campos['help'] : '',
                );
                $data['help'] .= " (Tamaño máximo de archivo " . $this->max_upload . ")";
                break;
            case 'multiple_image':
                $folder = $this->metadata['modulo'];
                $fields = array();
                if isset($fila[$campos['field']]):
                    $count = count($fila[$campos['field']]);
                    foreach ($fila[$campos['field']] as $key : $campo:
                        $field                = $campo;
                        $field['title_field'] = $campos['title_field'];
                        $field['field']       = $campos['field'];
                        $field['image']       = image.generar_url($campo, 'thumb');
                        $field['active']      = $campo['portada'];
                        $field['class']       = ('true' == $campo['portada']) ? 'btn-success' : 'btn-danger';
                        $field['icon']        = ('true' == $campo['portada']) ? 'fa-check' : 'fa-close';
                        $fields[]             = $field;
                    }
                } else {
                    $count = 0;
                }

                $data = array(
                    'title_field' : $campos['title_field'],
                    'field'       : $campos['field'],
                    'is_required' : $campos['required'],
                    'help'        : $campos['help'],
                    'required'    : ($campos['required']) ? 'required="required"' : '',
                    'fields'      : $fields,
                    'count'       : ($count > 0) ? $count : '',
                );
                break;
            case 'file':
                $folder   = $this->metadata['modulo'];
                $file_url = (isset($fila[$campos['field']]) && isset($fila[$campos['field']][0])) ? (file.generar_url($fila[$campos['field']][0], '')) : '';
                $data     = array(
                    'title_field'       : $campos['title_field'],
                    'field'             : $campos['field'],
                    'is_required'       : $campos['required'],
                    'is_required_modal' : ('' != $file_url) ? $campos['required'] : true,
                    'is_required_alert' : ('' != $file_url) ? $campos['required'] : true,
                    'required'          : ($campos['required']) ? 'required="required"' : '',
                    'file'              : $file_url,
                    'is_file'           : ('' != $file_url) ? true : false,
                    'url'               : ('' != $file_url) ? $fila[$campos['field']][0]['url'] : '',
                    'parent'            : ('' != $file_url) ? $fila[$campos['field']][0]['parent'] : '',
                    'folder'            : ('' != $file_url) ? $fila[$campos['field']][0]['folder'] : '',
                    'subfolder'         : ('' != $file_url) ? $fila[$campos['field']][0]['subfolder'] : '',
                    'help'              : (isset($campos['help'])) ? $campos['help'] : '',
                );
                $data['help'] .= " (Tamaño máximo de archivo " . $this->max_upload . ")";
                break;
            case 'multiple_file':
                $folder = $this->metadata['modulo'];
                $fields = array();
                if isset($fila[$campos['field']]):
                    foreach ($fila[$campos['field']] as $key : $campo:
                        $field                = $campo;
                        $field['title_field'] = $campos['title_field'];
                        $field['field']       = $campos['field'];
                        $field['file']        = file.generar_url($campo, '');
                        $fields[]             = $field;
                    }
                }

                $data = array(
                    'title_field' : $campos['title_field'],
                    'field'       : $campos['field'],
                    'is_required' : $campos['required'],
                    'help'        : (isset($campos['help'])) ? $campos['help'] : '',
                    'required'    : ($campos['required']) ? 'required="required"' : '',
                    'fields'      : $fields,
                );
                $data['help'] .= " (Tamaño máximo de archivo " . $this->max_upload . ")";
                break;
            case 'number':
                $data = array(
                    'title_field' : $campos['title_field'],
                    'field'       : $campos['field'],
                    'is_required' : $campos['required'],
                    'required'    : ($campos['required']) ? 'required="required"' : '',
                    'value'       : (isset($fila[$campos['field']])) ? $fila[$campos['field']] : '',
                    'help'        : (isset($campos['help'])) ? $campos['help'] : '',
                );
                break;
            case 'email':
                $data = array(
                    'title_field' : $campos['title_field'],
                    'field'       : $campos['field'],
                    'is_required' : $campos['required'],
                    'required'    : ($campos['required']) ? 'required="required"' : '',
                    'value'       : (isset($fila[$campos['field']])) ? $fila[$campos['field']] : '',
                );
                break;
            case 'password':
                $data = array(
                    'title_field' : $campos['title_field'],
                    'field'       : $campos['field'],
                    'is_required' : $campos['required'],
                    'required'    : ($campos['required']) ? 'required="required"' : '',
                );
                break;
            case 'token':
                $data = array(
                    'title_field' : $campos['title_field'],
                    'field'       : $campos['field'],
                    'is_required' : $campos['required'],
                    'required'    : ($campos['required']) ? 'required="required"' : '',
                    'value'       : (isset($fila[$campos['field']])) ? $fila[$campos['field']] : '',
                );
                break;
            case 'map':
                $data = array(
                    'title_field' : $campos['title_field'],
                    'field'       : $campos['field'],
                    'is_required' : $campos['required'],
                    'required'    : ($campos['required']) ? 'required="required"' : '',
                    'direccion'   : (isset($fila[$campos['field']])) ? $fila[$campos['field']]['direccion'] : '',
                    'lat'         : (isset($fila[$campos['field']])) ? $fila[$campos['field']]['lat'] : '',
                    'lng'         : (isset($fila[$campos['field']])) ? $fila[$campos['field']]['lng'] : '',
                );
                break;
            case 'recursive_checkbox':
            case 'recursive_radio':
                if 0 == $level:
                    if isset($fila[$campos['field']]):
                        $count = count($fila[$campos['field']]);
                    } else {
                        if 'recursive_radio' == $campos['type'] || isset($app.get[$campos['field']]):
                            $count = 1;
                        } else {
                            $count = 0;
                        }
                    }
                    $data = array(
                        'is_children' : false,
                        'title_field' : $campos['title_field'],
                        'field'       : $campos['field'],
                        'is_required' : $campos['required'],
                        'children'    : '',
                        'required'    : ($campos['required']) ? 'required="required"' : '',
                        'count'       : ($count > 0) ? $count : '',
                    );
                    foreach ($campos['parent'] as $key : $children:
                        $data['children'] .= $this->field($campos, $fila, '', $children[0], 1);
                    }
                } else {
                    $parent  = $campos['parent'];
                    $checked = (0 == $idparent) ? 'checked="checked"' : '';
                    if !isset($fila[$campos['field']]):
                        if isset($app.get[$campos['field']]):
                            $checked = ($idparent == $app.get[$campos['field']]) ? 'checked="checked"' : '';
                        }
                    } else {
                        $checked = (in_array($idparent, $fila[$campos['field']])) ? 'checked="checked"' : '';
                    }
                    $data = array(
                        'is_children' : true,
                        'field'       : $campos['field'],
                        'value'       : $idparent,
                        'title'       : (isset($parent[$idparent])) ? $parent[$idparent]['titulo'] : '',
                        'checked'     : $checked,
                        'required'    : ($campos['required']) ? 'required' : '',
                        'level'       : ($level - 1) * 20,
                        'children'    : '',
                    );
                    if isset($parent[$idparent]):
                        $campos['parent'] = $parent[$idparent]['children'];
                        foreach ($campos['parent'] as $key : $children:
                            $data['children'] .= $this->field($campos, $fila, '', $children[0], $level + 1);
                        }
                    }
                }
                break;
            case 'select':
                $data = array(
                    'title_field' : $campos['title_field'],
                    'field'       : $campos['field'],
                    'is_required' : $campos['required'],
                    'required'    : ($campos['required']) ? 'required="required"' : '',
                    'help'        : (isset($campos['help'])) ? $campos['help'] : '',
                    'option'      : array(),
                );
                foreach ($campos['parent'] as $key : $children:
                    $selected = (0 == $children[0]) ? 'selected="selected"' : '';
                    if !isset($fila[$campos['field']]):
                        if isset($app.get[$campos['field']]):
                            $selected = ($children[0] == $app.get[$campos['field']]) ? 'selected="selected"' : '';
                        }
                    } else {
                        $selected = ($children[0] == $fila[$campos['field']]) ? 'selected="selected"' : '';
                    }

                    $data['option'][] = array('value' : $children[0], 'selected' : $selected, 'text' : $children['titulo']);
                }
                break;
            case 'textarea':
                $data = array(
                    'title_field' : $campos['title_field'],
                    'field'       : $campos['field'],
                    'is_required' : $campos['required'],
                    'required'    : ($campos['required']) ? 'required="required"' : '',
                    'value'       : (isset($fila[$campos['field']])) ? $fila[$campos['field']] : '',
                );
                break;
            case 'text':
            default:
                $data = array(
                    'title_field' : $campos['title_field'],
                    'field'       : $campos['field'],
                    'is_required' : $campos['required'],
                    'required'    : ($campos['required']) ? 'required="required"' : '',
                    'value'       : (isset($fila[$campos['field']])) ? $fila[$campos['field']] : '',
                    'help'        : (isset($campos['help'])) ? $campos['help'] : '',
                );
                break;
        }

        
        view.set_array($data);
        $content=view.render('detail/'.$campos['type'], false, true);
        return $content;
    }

    public static function guardar($class)
    {
        $campos    = $_POST['campos'];
        $respuesta = array('exito' : false, 'mensaje' : '');

        if '' == $campos['id']:
            $respuesta['id']      = $class.insert($campos);
            $respuesta['mensaje'] = "Creado correctamente";
        } else {
            $respuesta['id']      = $class.update($campos);
            $respuesta['mensaje'] = "Actualizado correctamente";
        }
        $respuesta['exito'] = true;
        if is_array($respuesta['id']):
            return $respuesta['id'];
        }
        return $respuesta;
    }
