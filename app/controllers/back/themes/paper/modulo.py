from .base import base
from app.models.modulo import modulo as modulo_model

#from app.models.table import table as table_model
#from app.models.administrador import administrador as administrador_model
#from app.models.modulo import modulo as modulo_model
from app.models.moduloconfiguracion import moduloconfiguracion as moduloconfiguracion_model

#from .detalle import detalle as detalle_class
#from .lista import lista as lista_class
#from .head import head
#from .header import header
#from .aside import aside
#from .footer import footer

from core.app import app
#from core.database import database
#from core.functions import functions
#from core.image import image


#import json

class modulo(base):
    url = ['modulo']
    metadata = {'title' : 'Modulos','modulo':'modulo'}
    breadcrumb = []
    parent_class = None
    parent = None
    tipos_recortes = {
        'recortar' : {'text' : 'Recortar', 'value' : 'recortar'},
        'rellenar' : {'text' : 'Rellenar', 'value' : 'rellenar'},
        'centrar' : {'text' : 'Centrar', 'value' : 'centrar'}
    }

    tipos_menu = {
        'new' : {'titulo' : 'Nuevo', 'field' : 'new'},
        'excel' : {'titulo' : 'Exportar a excel', 'field' : 'excel'},
        'regenerar' : {'titulo' : 'Regenerar imagenes', 'field' : 'regenerar'}
    }



    def __init__(self):
        super().__init__(modulo_model)
        self.parent_class = moduloconfiguracion_model()
        parent_class=self.parent_class

        if not 'idmoduloconfiguracion' in app.get:
            self.url = array('home')
        } else {
        self.parent = parent_class.getById(app.get['idmoduloconfiguracion'])
            array_pop(self.breadcrumb)
            self.breadcrumb[] = array('url' : functions.generar_url(array('moduloconfiguracion')), 'title' : self.parent['titulo'], 'active' : '')
            self.metadata['title'] = self.parent['titulo'] . ' - ' . self.metadata['title']
            self.breadcrumb[] = array('url' : functions.generar_url(self.url), 'title' : (self.metadata['title']), 'active' : 'active')
        }
    }
    public function index()
    {
        class = this->class // Clase para enviar a controlador de lista
        parent_class = this->parent_class // Clase Padre
        parent=this->parent
        
        if not administrador_model.verificar_sesion():
            this->url = array_merge(array('login', 'index'), this->url)
        }
        functions.url_redirect(this->url) //verificar sesion o redireccionar a login

        /* cabeceras y campos que se muestran en la lista:
        titulo,campo de la tabla a usar, tipo (ver archivo lista.php funcion "field") */
        th = array(
            'id' : array('title_th' : 'ID', 'field' : 0, 'type' : 'text'),
            'tipo' : array('title_th' : 'Tipo', 'field' : 'tipo', 'type' : 'text'),
            'orden' : array('title_th' : 'Orden', 'field' : 'orden', 'type' : 'text'),
            'titulo' : array('title_th' : 'Titulo', 'field' : 'titulo', 'type' : 'text'),
            'aside' : array('title_th' : 'Aparece en aside', 'field' : 'aside', 'type' : 'active'),
            //'hijos' : array('title_th' : 'Contiene hijos', 'field' : 'hijos', 'type' : 'active'),
            'copy' : array('title_th' : 'Copiar', 'field' : 0, 'type' : 'action','action':'copy','mensaje':'Copiando Elemento'),
            'editar' : array('title_th' : 'Editar', 'field' : 'url_detalle', 'type' : 'link'),
            'delete' : array('title_th' : 'Eliminar', 'field' : 'delete', 'type' : 'delete'),
        )

        list = new lista(this->metadata) //controlador de lista

        where = array('idmoduloconfiguracion' : parent[0])
        condiciones = array()
        url_detalle = this->url
        url_detalle[] = 'detail'
        respuesta = list->get_row(class, where, condiciones, url_detalle) //obtener unicamente elementos de la pagina actual
        row = respuesta['row']
        new = (parent['tipos'] || count(row) == 0) ? true : false
        menu = array('new' : new, 'excel' : false, 'regenerar' : false)

        data = array( //informacion para generar la vista de la lista, arrays SIEMPRE antes de otras variables!!!!
            'breadcrumb' : this->breadcrumb,
            'th' : th,
            'current_url' : functions.generar_url(this->url),
            'new_url' : functions.generar_url(url_detalle),
        )
        data = array_merge(data, respuesta, menu)
        list->normal(data)
    }

    public function detail(var = array())
    {
        class = this->class // Clase para enviar a controlador de detalle
        parent_class = this->parent_class // Clase Padre
        parent = this->parent // Clase Padre

        url_save = url_list = this->url
        url_save[] = 'guardar'
        this->url[] = 'detail'
        if (isset(var[0]):
            id = (int) var[0]
            this->url[] = id
            this->metadata['title'] = 'Editar '.this->metadata['title'] 
        } else {
            id = 0
            this->metadata['title'] = 'Nuevo '.this->metadata['title'] 
        }

        this->breadcrumb[] = array('url' : functions.generar_url(this->url), 'title' : (this->metadata['title']), 'active' : 'active')

        if not administrador_model.verificar_sesion():
            this->url = array_merge(array('login', 'index'), this->url)
        }
        functions.url_redirect(this->url) //verificar sesion o redireccionar a login

        this->metadata['title'] = parent['titulo'] . ' - ' . this->metadata['title']

        /* cabeceras y campos que se muestran en el detalle:
        titulo,campo de la tabla a usar, tipo (ver archivo detalle.php funcion "field") */

        ta = profile.getAll(array('estado' : true))
        tipos_administrador = array()
        foreach (ta as key : t:
            tipos_administrador[t['tipo']] = array('id' : t['tipo'], 'text' : t['titulo'])
        }

        columnas_menu = array(
            'field' : array('title_field' : 'Campo', 'field' : 'field', 'type' : 'multiple_hidden', 'required' : true),
            'titulo' : array('title_field' : 'Titulo', 'field' : 'titulo', 'type' : 'multiple_label', 'required' : true, 'col' : 3),
            'estado' : array('title_field' : 'Estado', 'field' : 'estado', 'type' : 'multiple_active_array', 'required' : true, 'col' : 9, 'array' : tipos_administrador),
        )
        columnas_mostrar = array(
            'field' : array('title_field' : 'Campo', 'field' : 'field', 'type' : 'multiple_hidden', 'required' : true),
            'tipo' : array('title_field' : 'Tipo', 'field' : 'tipo', 'type' : 'multiple_hidden', 'required' : true),
            'titulo' : array('title_field' : 'Titulo', 'field' : 'titulo', 'type' : 'multiple_label', 'required' : true, 'col' : 3),
            'estado' : array('title_field' : 'Estado', 'field' : 'estado', 'type' : 'multiple_active_array', 'required' : true, 'col' : 9, 'array' : tipos_administrador),
        )
        columnas_detalle = array(
            'field' : array('title_field' : 'Campo', 'field' : 'field', 'type' : 'multiple_hidden', 'required' : true),
            'tipo' : array('title_field' : 'Tipo', 'field' : 'tipo', 'type' : 'multiple_hidden', 'required' : true),
            'titulo' : array('title_field' : 'Titulo', 'field' : 'titulo', 'type' : 'multiple_label', 'required' : true, 'col' : 2),
            'texto_ayuda' : array('title_field' : 'Texto de ayuda', 'field' : 'texto_ayuda', 'type' : 'multiple_text', 'required' : false, 'col' : 2),
            'required' : array('title_field' : 'Obligatorio', 'field' : 'required', 'type' : 'multiple_active', 'required' : true, 'col' : 2),
            'estado' : array('title_field' : 'Estado', 'field' : 'estado', 'type' : 'multiple_active_array', 'required' : true, 'col' : 6, 'array' : tipos_administrador),
        )

        columnas_recortes = array(
            'tag' : array('title_field' : 'Etiqueta', 'field' : 'tag', 'type' : 'multiple_text', 'required' : true, 'col' : 2),
            'titulo' : array('title_field' : 'Titulo', 'field' : 'titulo', 'type' : 'multiple_text', 'required' : true, 'col' : 2),
            'ancho' : array('title_field' : 'Ancho', 'field' : 'ancho', 'type' : 'multiple_text', 'required' : true, 'col' : 1),
            'alto' : array('title_field' : 'Alto', 'field' : 'alto', 'type' : 'multiple_text', 'required' : true, 'col' : 1),
            'calidad' : array('title_field' : 'Calidad', 'field' : 'calidad', 'type' : 'multiple_number', 'required' : true, 'col' : 2, 'max' : 100, 'default' : 90),
            'tipo' : array('title_field' : 'Tipo', 'field' : 'tipo', 'type' : 'multiple_select', 'required' : true, 'option' : this->tipos_recortes, 'col' : 2),
            'button' : array('field' : '', 'type' : 'multiple_button', 'col' : 2),
        )
        columnas_estado = array(
            'estado' : array('title_field' : 'Estado', 'field' : 'estado', 'type' : 'multiple_active_array', 'required' : true, 'col' : 9, 'array' : tipos_administrador),
        )
        campos = array(
            'idmoduloconfiguracion' : array('title_field' : 'idmoduloconfiguracion', 'field' : 'idmoduloconfiguracion', 'type' : 'hidden', 'required' : true),
            'titulo' : array('title_field' : 'Titulo', 'field' : 'titulo', 'type' : 'text', 'required' : true),
            'menu' : array('title_field' : 'Menu', 'field' : 'menu', 'type' : 'multiple', 'required' : true, 'columnas' : columnas_menu),
            'mostrar' : array('title_field' : 'Mostrar', 'field' : 'mostrar', 'type' : 'multiple', 'required' : true, 'columnas' : columnas_mostrar),
            'detalle' : array('title_field' : 'Detalle', 'field' : 'detalle', 'type' : 'multiple', 'required' : true, 'columnas' : columnas_detalle),
            'recortes' : array('title_field' : 'Imagenes', 'field' : 'recortes', 'type' : 'multiple', 'required' : true, 'columnas' : columnas_recortes),
            'tipo' : array('title_field' : 'Tipo', 'field' : 'tipo', 'type' : 'number', 'required' : true),
            'orden' : array('title_field' : 'Orden', 'field' : 'orden', 'type' : 'number', 'required' : true),
            'estado' : array('title_field' : 'Estado', 'field' : 'estado', 'type' : 'multiple', 'required' : true, 'columnas' : columnas_estado),
            'aside' : array('title_field' : 'Aside', 'field' : 'aside', 'type' : 'active', 'required' : true),
            'hijos' : array('title_field' : 'Contiene hijos', 'field' : 'hijos', 'type' : 'active', 'required' : true),
        )

        detalle = new detalle(this->metadata) //controlador de detalle
        row = (id != 0) ? (class.getById(id)) : array()
        if not parent['tipos']:
            campos['tipo']['type'] = 'hidden'
            row['tipo'] = 0
        }

        if (isset(row['menu']):
            foreach (row['menu'] as key : m:
                row['menu'][m['field']] = m
            }
        }
        menu = array()
        foreach (this->tipos_menu as key : p:
            t = array()
            if (isset(row['menu']) && isset(row['menu'][p['field']]):
                t = row['menu'][p['field']]
            }
            t = array_merge(t, p)
            menu[] = t
        }
        row['menu'] = menu

        if (isset(row['mostrar']):
            foreach (row['mostrar'] as key : m:
                row['mostrar'][m['field']] = m
            }
        }

        mostrar = array()
        if (is_array(parent['mostrar']):
            foreach (parent['mostrar'] as key : p:
                t = array()
                if (isset(row['mostrar']) && isset(row['mostrar'][p['field']]):
                    t = row['mostrar'][p['field']]
                }
                t = array_merge(t, p)
                mostrar[] = t
            }
        }
        row['mostrar'] = mostrar

        if (isset(row['detalle']):
            foreach (row['detalle'] as key : m:
                row['detalle'][m['field']] = m
            }
        }
        det = array()
        if (is_array(parent['detalle']):
            foreach (parent['detalle'] as key : d:
                t = array()
                if (isset(row['detalle']) && isset(row['detalle'][d['field']]):
                    t = row['detalle'][d['field']]
                }
                t = array_merge(t, d)
                det[] = t
            }
        }

        row['detalle'] = det

        if (id == 0:
            estados = array()
            foreach (tipos_administrador as key : ta:
                estados[key] = "true"
            }
            row['estado'] = array(array('estado' : estados))
        }

        row['idmoduloconfiguracion'] = parent[0]

        data = array( //informacion para generar la vista del detalle, arrays SIEMPRE antes de otras variables!!!!
            'breadcrumb' : this->breadcrumb,
            'campos' : campos,
            'row' : row,
            'id' : (id != 0) ? id : '',
            'current_url' : functions.generar_url(this->url),
            'save_url' : functions.generar_url(url_save),
            'list_url' : functions.generar_url(url_list),
        )

        detalle->normal(data, class)
    }

}
