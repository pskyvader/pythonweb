from core.app import app
from core.file import file
from core.image import image
from core.view import view
from .head import head
from .header import header
from .aside import aside
from .footer import footer


from app.models.moduloconfiguracion import moduloconfiguracion as moduloconfiguracion_model
from app.models.modulo import modulo as modulo_model

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
    def configuracion(self,modulo, force = False):
        tipo_admin          = app.session["tipo" + app.prefix_site]
        moduloconfiguracion = moduloconfiguracion_model.getByModulo(modulo)
        var                 = {'idmoduloconfiguracion' : moduloconfiguracion[0]}
        if 'tipo' in app.get:
            var['tipo'] = app.get['tipo']
        
        modulo  = modulo_model.getAll(var, {'limit' : 1})
        modulo  = modulo[0]
        estados = modulo['estado'][0]['estado']
        if 'True' != estados[tipo_admin] and not force:
            return {'error': 301, 'redirect': functions.url_redirect(['home'])}
        
        campos = {}
        for m in modulo['detalle']:
            if 'True' == m['estado'][tipo_admin]:
                campos[m['field']] = {'title_field' : m['titulo'], 'field' : m['field'], 'type' : m['tipo'], 'required' : ('True' == m['required']), 'help' : m['texto_ayuda']}
           

        return {'campos' : campos}




    def field(self,campos, fila, parent = '', idparent = 0, level = 0):
        import datetime
        editor_count = 0
        if campos['type']=='active':
            data = {
                'title_field' : campos['title_field'],
                'field'       : campos['field'],
                'required' : campos['required'],
                'active'      : fila[campos['field']] if campos['field'] in fila else '' ,
                'class'       : ('btn-success' if fila[campos['field']] else 'btn-danger') if campos['field'] in fila else 'btn-default',
                'icon'       : ('fa-check' if fila[campos['field']] else 'fa-close') if campos['field'] in fila else 'fa-question-circle',
            }
        elif campos['type']=='color':
            data = {
                'title_field' : campos['title_field'],
                'field'       : campos['field'],
                'required' : campos['required'],
                'help'      : fila[campos['help']] if campos['help'] in fila else '' ,
                'value'      : fila[campos['field']] if campos['field'] in fila else '' ,
            }
        elif campos['type']=='date':
            data = {
                'title_field' : campos['title_field'],
                'field'       : campos['field'],
                'required' : campos['required'],
                'help'      : fila[campos['help']] if campos['help'] in fila else '' ,
                'value'      : fila[campos['field']] if campos['field'] in fila else '' ,
            }
        elif campos['type']=='daterange':
            data = {
                'title_field' : campos['title_field'],
                'field'       : campos['field'],
                'required' : campos['required'],
                'help'      : fila[campos['help']] if campos['help'] in fila else '' ,
                'value'      : fila[campos['field']] if campos['field'] in fila else '' ,
            }
        elif campos['type']=='editor':
            data = {
                'title_field' : campos['title_field'],
                'field'       : campos['field'],
                'required' : campos['required'],
                'help'      : fila[campos['help']] if campos['help'] in fila else '' ,
                'value'      : fila[campos['field']] if campos['field'] in fila else '' ,
            }
            data['help'] += " (Tamaño máximo de archivo " +self.max_upload + ")"
            if 0 == editor_count:
                theme           = app.get_url() + view.get_theme() + 'assets/ckeditor/'
                t               = '?t=I8BG'
                data['preload'] = [
                    {'url' : 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css', 'type' : 'style'},
                    {'url' : 'https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css', 'type' : 'style'},
                    {'url' : 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js', 'type' : 'script'},
                    {'url' : 'https://code.jquery.com/jquery-1.11.3.min.js', 'type' : 'script'},

                    {'url' : theme + 'contents.css', 'type' : 'style'},
                    {'url' : theme + 'plugins/btgrid/styles/editor.css', 'type' : 'style'},
                    {'url' : theme + 'plugins/tableselection/styles/tableselection.css', 'type' : 'style'},
                    {'url' : theme + 'plugins/balloontoolbar/skins/default.css', 'type' : 'style'},
                    {'url' : theme + 'plugins/balloontoolbar/skins/moono-lisa/balloontoolbar.css', 'type' : 'style'},
                    {'url' : theme + 'plugins/balloonpanel/skins/moono-lisa/balloonpanel.css', 'type' : 'style'},

                    {'url' : theme + 'skins/moono-lisa/editor.css' . t, 'type' : 'style'},
                    {'url' : theme + 'plugins/basewidget/css/style.css' . t, 'type' : 'style'},
                    {'url' : theme + 'plugins/layoutmanager/css/style.css' . t, 'type' : 'style'},
                ]

            else:
                data['preload'] = []
            
            editor_count+=1
            
        elif campos['type']=='grupo_pedido':
            folder      = self.metadata['modulo']
            direcciones = []
            if campos['field'] in fila:
                count = count(fila[campos['field']])
                for campo in fila[campos['field']]:
                    field                = campo
                    field['title_field'] = campos['title_field']
                    field['field']       = campos['field']
                    direcciones.append(field)
                
            else:
                count = 0
            
            for d in direcciones:
                d['lista_productos']   = campos['lista_productos']
                d['direccion_entrega'] = campos['direccion_entrega']
                for e in d['direccion_entrega']:
                    if e['idusuariodireccion'] == d['idusuariodireccion']:
                        e['selected'] = 'selected=""'
                    else:
                        e['selected'] = ''

                for p in d['productos'] :
                    p['lista_atributos'] = campos['lista_atributos']
                    for e in p['lista_atributos']:
                        if e['idproducto'] == p['idproductoatributo']:
                            e['selected'] = 'selected=""'
                        else:
                            e['selected'] = ''
                            
            data = {
                'title_field'       : campos['title_field'],
                'field'             : campos['field'],
                'required'       : campos['required'],
                'help'              : campos['help'],
                'direcciones'       : direcciones,
                'direccion_entrega' : campos['direccion_entrega'],
                'lista_productos'   : campos['lista_productos'],
                'lista_atributos'   : campos['lista_atributos'],
                'fecha'             : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'count'             : str(count) if count > 0 else '',
            }

        elif campos['type']=='multiple':
            fields = []
            count  =  len(fila[campos['field']]) if campos['field'] in fila and isinstance(fila[campos['field']], dict) else 0
            if count > 0:
                for f in fila[campos['field']]:
                    td = []
                    for v in campos['columnas']:
                        content = self.field(v, f, campos['field'], key)
                        td.append({'content' : content, 'content_field' : v['field']})
                    
                    linea    = {'columna' : td}
                    fields.append(linea)
                
                new_field = False
            else:
                new_field = True
            
            new_line = []
            for v in campos['columnas']:
                content    = self.field(v, {}, campos['field'])
                new_line.append({'content' : content, 'content_field' : v['field']})
            

            data = {
                'fields'      : fields,
                'count'       : count,
                'new_field'   : new_field,
                'new_line'    : new_line,
                'title_field' : campos['title_field'],
                'field'       : campos['field'],
                'required' : campos['required'],
            }
        elif campos['type']=='multiple_text':
            data = {
                'title_field' : campos['title_field'],
                'field'       : campos['field'],
                'parent'      : parent,
                'col'         : campos['col'],
                'required' : campos['required'],
                'value'      : fila[campos['field']] if campos['field'] in fila else '' ,
            }
        elif campos['type']=='multiple_number':
            data = {
                'title_field' : campos['title_field'],
                'field'       : campos['field'],
                'parent'      : parent,
                'col'         : campos['col'],
                'max'         : campos['max'],
                'required' : campos['required'],
                'value'       : fila[campos['field']] if campos['field'] in fila else campos['default'],
            }
        elif campos['type']=='multiple_label':
            data = {
                'title_field' : campos['title_field'],
                'field'       : campos['field'],
                'parent'      : parent,
                'col'         : campos['col'],
                'required' : campos['required'],
                'value'      : fila[campos['field']] if campos['field'] in fila else '' ,
            }
        
        elif campos['type']=='multiple_hidden':
            data = {
                'field'    : campos['field'],
                'parent'   : parent,
                'required' : campos['required'],
                'value'      : fila[campos['field']] if campos['field'] in fila else '' ,
            }
        elif campos['type']=='multiple_select':
            for option in campos['option']:
                option['selected'] = 'selected="selected"' if campos['field'] in fila and fila[campos['field']] == option['value'] else ''
            
            data = {
                'title_field' : campos['title_field'],
                'field'       : campos['field'],
                'parent'      : parent,
                'col'         : campos['col'],
                'option'      : campos['option'],
                'required' : campos['required'],
            }
        elif campos['type']=='multiple_button':
            data = {
                'col' : campos['col'],
            }
        elif campos['type']=='multiple_order':
            data = {
                'col' : campos['col'],
            }
        elif campos['type']=='multiple_active':
            data = {
                'title_field' : campos['title_field'],
                'field'       : campos['field'],
                'parent'      : parent,
                'col'         : campos['col'],
                'required' : campos['required'],
                'active'      : str(fila[campos['field']]) if campos['field'] in fila else '' ,
                'class'       : ('btn-success' if fila[campos['field']]=='true' else 'btn-danger') if campos['field'] in fila else 'btn-default',
                'icon'       : ('fa-check' if fila[campos['field']]=='true' else 'fa-close') if campos['field'] in fila else 'fa-question-circle',
            }
        elif campos['type']=='multiple_active_array':
            for value in campos['array']:
                value['active'] = str(fila[campos['field']]) if campos['field'] in fila else 'true',
                value['class']  = ('btn-success' if fila[campos['field']]=='true' else 'btn-danger') if campos['field'] in fila else 'btn-success',
                value['icon']   = ('fa-check' if fila[campos['field']]=='true' else 'fa-close') if campos['field'] in fila else 'fa-check',
            
            data = {
                'title_field' : campos['title_field'],
                'array'       : campos['array'],
                'field'       : campos['field'],
                'idparent'    : idparent,
                'parent'      : parent,
                'col'         : campos['col'],
                'required' : campos['required'],
            }
        elif campos['type']=='image':
            folder    = self.metadata['modulo']
            image_url = image.generar_url(fila[campos['field']][0], 'thumb') if campos['field'] in fila and 0 in fila[campos['field']] else ''
            data      = {
                'title_field'       : campos['title_field'],
                'field'             : campos['field'],
                'required'       : campos['required'],
                'image'             : image_url,
                'is_image'          : '' != image_url,
                'url'               :  fila[campos['field']][0]['url'] if '' != image_url else '',
                'parent'            :  fila[campos['field']][0]['parent'] if '' != image_url else '',
                'folder'            :  fila[campos['field']][0]['folder'] if '' != image_url else '',
                'subfolder'         :  fila[campos['field']][0]['subfolder'] if '' != image_url else '',
                'help'              : campos['help'] if 'help' in campos else '',
            }
            data['help'] += " (Tamaño máximo de archivo " + self.max_upload + ")"
            
        elif campos['type']=='multiple_image':
            folder = self.metadata['modulo']
            fields = []
            if campos['field'] in fila:
                count = len(fila[campos['field']])
                for campo in fila[campos['field']]:
                    field                = campo
                    field['title_field'] = campos['title_field']
                    field['field']       = campos['field']
                    field['image']       = image.generar_url(campo, 'thumb')
                    field['active']      = campo['portada']
                    field['class']       ='btn-success' if 'true' == campo['portada'] else 'btn-danger'
                    field['icon']        = 'fa-check' if 'true' == campo['portada'] else 'fa-close'
                    fields.append(field)
            else:
                count = 0

            data = {
                'title_field' : campos['title_field'],
                'field'       : campos['field'],
                'required' : campos['required'],
                'help'        : campos['help'],
                'fields'      : fields,
                'count'       : count if count>0 else ''
            }
        elif campos['type']=='file':
            folder   = self.metadata['modulo']
            file_url = file.generar_url(fila[campos['field']][0], '') if campos['field'] in fila and 0 in fila[campos['field']] else ''
            data     = {
                'title_field'       : campos['title_field'],
                'field'             : campos['field'],
                'required'       : campos['required'],
                'file'              : file_url,
                'is_file'           : '' != file_url,
                'url'               :  fila[campos['field']][0]['url'] if '' != file_url else '',
                'parent'            :  fila[campos['field']][0]['parent'] if '' != file_url else '',
                'folder'            :  fila[campos['field']][0]['folder'] if '' != file_url else '',
                'subfolder'         :  fila[campos['field']][0]['subfolder'] if '' != file_url else '',
                'help'              : campos['help'] if 'help' in campos else '',
            }
            data['help'] += " (Tamaño máximo de archivo " + self.max_upload + ")"
            
        elif campos['type']=='multiple_file':
            folder = self.metadata['modulo']
            fields = []
            if campos['field'] in fila:
                for campo in fila[campos['field']]:
                    field                = campo
                    field['title_field'] = campos['title_field']
                    field['field']       = campos['field']
                    field['file']        = file.generar_url(campo, '')
                    
                    fields.append(field)

            data = {
                'title_field' : campos['title_field'],
                'field'       : campos['field'],
                'required' : campos['required'],
                'help'              : campos['help'] if 'help' in campos else '',
                'fields'      : fields,
            }
            data['help'] += " (Tamaño máximo de archivo " + self.max_upload + ")"

        elif campos['type']=='number':
            data = {
                'title_field' : campos['title_field'],
                'field'       : campos['field'],
                'required' : campos['required'],
                'value'      : fila[campos['field']] if campos['field'] in fila else '' ,
                'help'              : campos['help'] if 'help' in campos else '',
            }
        elif campos['type']=='email':
        case 'email':
            data = {
                'title_field' : campos['title_field'],
                'field'       : campos['field'],
                'required' : campos['required'],
                'value'      : fila[campos['field']] if campos['field'] in fila else '' ,
            }
        case 'password':
            data = {
                'title_field' : campos['title_field'],
                'field'       : campos['field'],
                'required' : campos['required'],
            }
        case 'token':
            data = {
                'title_field' : campos['title_field'],
                'field'       : campos['field'],
                'required' : campos['required'],
                'value'      : fila[campos['field']] if campos['field'] in fila else '' ,
            }
        case 'map':
            data = {
                'title_field' : campos['title_field'],
                'field'       : campos['field'],
                'required' : campos['required'],
                'direccion'   : (isset(fila[campos['field']])) ? fila[campos['field']]['direccion'] : '',
                'lat'         : (isset(fila[campos['field']])) ? fila[campos['field']]['lat'] : '',
                'lng'         : (isset(fila[campos['field']])) ? fila[campos['field']]['lng'] : '',
            }
        case 'recursive_checkbox':
        case 'recursive_radio':
            if 0 == level:
                if isset(fila[campos['field']]):
                    count = count(fila[campos['field']])
                else:
                    if 'recursive_radio' == campos['type'] || isset(app.get[campos['field']]):
                        count = 1
                    else:
                        count = 0
                    }
                }
                data = {
                    'is_children' : False,
                    'title_field' : campos['title_field'],
                    'field'       : campos['field'],
                    'is_required' : campos['required'],
                    'children'    : '',
                    'required'    : (campos['required']) ? 'required="required"' : '',
                    'count'       : (count > 0) ? count : '',
                )
                foreach (campos['parent'] as key : children:
                    data['children'] .= self.field(campos, fila, '', children[0], 1)
                }
            else:
                parent  = campos['parent']
                checked = (0 == idparent) ? 'checked="checked"' : ''
                if !isset(fila[campos['field']]):
                    if isset(app.get[campos['field']]):
                        checked = (idparent == app.get[campos['field']]) ? 'checked="checked"' : ''
                    }
                else:
                    checked = (in_array(idparent, fila[campos['field']])) ? 'checked="checked"' : ''
                }
                data = {
                    'is_children' : True,
                    'field'       : campos['field'],
                    'value'       : idparent,
                    'title'       : (isset(parent[idparent])) ? parent[idparent]['titulo'] : '',
                    'checked'     : checked,
                    'required'    : campos['required'],
                    'level'       : (level - 1) * 20,
                    'children'    : '',
                )
                if isset(parent[idparent]):
                    campos['parent'] = parent[idparent]['children']
                    foreach (campos['parent'] as key : children:
                        data['children'] .= self.field(campos, fila, '', children[0], level + 1)
                    }
                }
            }
            break
        case 'select':
            data = {
                'title_field' : campos['title_field'],
                'field'       : campos['field'],
                'required' : campos['required'],
                'help'        : (isset(campos['help'])) ? campos['help'] : '',
                'option'      : array(),
            )
            foreach (campos['parent'] as key : children:
                selected = (0 == children[0]) ? 'selected="selected"' : ''
                if !isset(fila[campos['field']]):
                    if isset(app.get[campos['field']]):
                        selected = (children[0] == app.get[campos['field']]) ? 'selected="selected"' : ''
                    }
                else:
                    selected = (children[0] == fila[campos['field']]) ? 'selected="selected"' : ''
                }

                data['option'][] = array('value' : children[0], 'selected' : selected, 'text' : children['titulo'])
            }
            break
        case 'textarea':
            data = {
                'title_field' : campos['title_field'],
                'field'       : campos['field'],
                'required' : campos['required'],
                'value'      : fila[campos['field']] if campos['field'] in fila else '' ,
            }
        case 'text':
        default:
            data = {
                'title_field' : campos['title_field'],
                'field'       : campos['field'],
                'required' : campos['required'],
                'value'      : fila[campos['field']] if campos['field'] in fila else '' ,
                'help'        : (isset(campos['help'])) ? campos['help'] : '',
            }
        }

        
        view.set_array(data)
        content=view.render('detail/'.campos['type'], False, True)
        return content
    }

    public static function guardar(class)
    {
        campos    = _POST['campos']
        respuesta = array('exito' : False, 'mensaje' : '')

        if '' == campos['id']:
            respuesta['id']      = class.insert(campos)
            respuesta['mensaje'] = "Creado correctamente"
        else:
            respuesta['id']      = class.update(campos)
            respuesta['mensaje'] = "Actualizado correctamente"
        }
        respuesta['exito'] = True
        if is_array(respuesta['id']):
            return respuesta['id']
        }
        return respuesta
    }
