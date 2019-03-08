from .base import base

from app.models.table import table as table_model
from app.models.administrador import administrador as administrador_model
from app.models.configuracion import configuracion as configuracion_model
from app.models.modulo import modulo as modulo_model
from app.models.moduloconfiguracion import moduloconfiguracion as moduloconfiguracion_model

#from .detalle import detalle as detalle_class
#from .lista import lista as lista_class
from .head import head
from .header import header
from .aside import aside
from .footer import footer

from core.app import app
from core.database import database
from core.cache import cache
from core.functions import functions
#from core.image import image

import json


class configuracionadministrador(base):
    url = ['configuracionadministrador']
    metadata = {'title': 'Configuracion de administrador',
                'modulo': 'configuracionadministrador'}
    breadcrumb = []

    def __init__(self):
        super().__init__(None)

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

        vaciar = table_model.getAll({'truncate': True}, {}, 'tablename')
        data = {}
        data['vaciar'] = vaciar
        data['breadcrumb'] = cls.breadcrumb
        data['title'] = cls.metadata['title']
        data['save_url'] = functions.generar_url(cls.url + ['vaciar'])
        data['list_url'] = functions.generar_url(cls.url)

        ret['body'].append(('configuracion_administrador', data))

        f = footer()
        ret['body'] += f.normal()['body']

        return ret

    def vaciar(self):
        ret = {'body': []}
        post = app.post
        if 'campos' in post:
            campos = post['campos']
            respuesta = table_model.truncate(campos)
            cache.delete_cache()
        else:
            respuesta = {'exito': False,
                         'mensaje': 'Debe seleccionar una tabla para vaciar'}
        ret['body'] = json.dumps(respuesta)
        return ret

    def json(self,responder = True):
        respuesta = {'exito' : True, 'mensaje' : 'JSON generado correctamente'}
        ret = {'body': []}
        
        base_dir       = app.get_dir(True) + '/config/'
        row       = table_model.getAll()
        campos    = []
        for tabla in row.values():
            a = {
                'tablename' : tabla['tablename'],
                'idname'    : tabla['idname'],
                'fields'    : tabla['fields'],
                'truncate'  : tabla['truncate'],
            }
            campos.append(a)

        file_write = open(base_dir + 'bdd.json', 'w')
        file_write.write(json.dumps(campos))
        file_write.close()

        row         = moduloconfiguracion_model.getAll()
        campos      = []
        fields      = table_model.getByname('moduloconfiguracion')
        fields_hijo = table_model.getByname('modulo')
        for tabla in row.values():
            a        = database.create_data(fields, tabla)
            row_hijo = modulo_model.getAll({'idmoduloconfiguracion' : tabla[0]})
            h        = []

            for hijos in row_hijo.values():
                h.append(database.create_data(fields_hijo, hijos))
            
            a['hijo'] = h
            campos.append(a)
            

        file_write = open(base_dir + 'moduloconfiguracion.json', 'w')
        file_write.write(json.dumps(campos))
        file_write.close()

        row    = configuracion_model.getAll()
        campos = []
        fields = table_model.getByname('configuracion')
        for tabla in row.values():
            a        = database.create_data(fields, tabla)
            campos.append(a)

        file_write = open(base_dir + 'configuracion.json', 'w')
        file_write.write(json.dumps(campos))
        file_write.close()
        
        if responder:
            ret['body'] = json.dumps(respuesta)
            return ret
        else:
            return responder


    def json_update(self,responder = True):
        respuesta = {'exito' : True, 'mensaje' : ['JSON actualizado correctamente']}
        ret = {'body': []}

        base_dir       = app.get_dir(True) + '/config/'

        file_read = open(base_dir + 'bdd.json', 'r')
        campos=json.loads(file_read.read())
        file_read.close()
        
        for key,tabla in campos.items():
            tablename = tabla['tablename']
            #primero es siempre la tabla "tablas", se crea inmediatamente para guardar las siguientes configuraciones
            if key == 0: 
                existe = table_model.table_exists(tablename)
                if not existe:
                    fields = dict(tabla['fields'])
                    fields={'titulo' : tabla['idname'], 'tipo' : 'int(11)', 'primary' : True} +fields

                    foreach (fields as key : value:
                        if not isset(fields[key]['primary']):
                            fields[key]['primary'] = false
                        }
                    }
                    connection = database.instance()
                    connection->create(tablename, fields)
                }
            }
            table = table_model.getAll(array('tablename' : tablename))

            tabla['fields'] = functions.encode_json(tabla['fields'])
            if count(table) == 1:
                tabla['id'] = table[0][0]
                table_model.update(tabla, false)
            } else {
                table_model.insert(tabla, false)
            }
        }

        tablas = table_model.getAll()

        foreach (tablas as key : tabla:
            mensajes = table_model.validate(tabla[0], false)
            if not mensajes['exito']:
                respuesta = mensajes
                break
            } else {
                respuesta['mensaje'] = array_merge(respuesta['mensaje'], mensajes['mensaje'])
            }
        }

        row = administrador_model.getAll(array('email' : 'admin@mysitio.cl'))
        if count(row) == 0:
            insert_admin = array(
                'pass'         : 12345678,
                'pass_repetir' : 12345678,
                'nombre'       : 'Admin',
                'email'        : 'admin@mysitio.cl',
                'tipo'         : 1,
                'estado'       : True,
            )
            administrador_model.insert(insert_admin)
        }

        row = logo_model.getAll()
        if count(row) == 0:
            insert_logo = array(
                array('titulo' : 'favicon', 'orden' : 1),
                array('titulo' : 'Logo login', 'orden' : 2),
                array('titulo' : 'Logo panel grande', 'orden' : 3),
                array('titulo' : 'Logo panel pequeño', 'orden' : 4),
                array('titulo' : 'Logo Header sitio', 'orden' : 5),
                array('titulo' : 'Logo Footer sitio', 'orden' : 6),
                array('titulo' : 'Manifest', 'orden' : 7),
                array('titulo' : 'Email', 'orden' : 8),
            )
            foreach (insert_logo as key : logos:
                logo_model.insert(logos)
            }
        }

        campos = functions.decode_json(file_get_contents(base_dir . 'moduloconfiguracion.json'))
        foreach (campos as key : moduloconfiguracion:
            row  = moduloconfiguracion_model.getAll(array('module' : moduloconfiguracion['module']), array('limit' : 1))
            hijo = moduloconfiguracion['hijo']
            unset(moduloconfiguracion['hijo'])
            moduloconfiguracion['mostrar'] = functions.encode_json(moduloconfiguracion['mostrar'])
            moduloconfiguracion['detalle'] = functions.encode_json(moduloconfiguracion['detalle'])
            if count(row) == 1:
                moduloconfiguracion['id'] = row[0][0]
                moduloconfiguracion_model.update(moduloconfiguracion, false)
                foreach (hijo as key : h:
                    h['idmoduloconfiguracion'] = moduloconfiguracion['id']
                    row2                       = modulo_model.getAll(array('idmoduloconfiguracion' : h['idmoduloconfiguracion'], 'tipo' : h['tipo']), array('limit' : 1))

                    h['menu']     = functions.encode_json(h['menu'])
                    h['mostrar']  = functions.encode_json(h['mostrar'])
                    h['detalle']  = functions.encode_json(h['detalle'])
                    h['recortes'] = functions.encode_json(h['recortes'])
                    h['estado']   = functions.encode_json(h['estado'])
                    if count(row2) == 1:
                        h['id'] = row2[0][0]
                        modulo_model.update(h, false)
                    } else {
                        modulo_model.insert(h, false)
                    }
                }
            } else {
                id = moduloconfiguracion_model.insert(moduloconfiguracion, false)
                foreach (hijo as key : h:
                    h['idmoduloconfiguracion'] = id
                    h['menu']                  = functions.encode_json(h['menu'])
                    h['mostrar']               = functions.encode_json(h['mostrar'])
                    h['detalle']               = functions.encode_json(h['detalle'])
                    h['recortes']              = functions.encode_json(h['recortes'])
                    h['estado']                = functions.encode_json(h['estado'])
                    modulo_model.insert(h, false)
                }
            }
        }

        campos = functions.decode_json(file_get_contents(base_dir . 'configuracion.json'))
        foreach (campos as key : configuracion:
            row = configuracion_model.getByVariable(configuracion['variable'])
            configuracion_model.setByVariable(configuracion['variable'], configuracion['valor'])
        }
        cache.delete_cache()
        if responder:
            echo json_encode(respuesta)
        }
    }