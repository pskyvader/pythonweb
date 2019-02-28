from core.database import database
from .base_model import base_model


class log(base_model):
    idname = 'idlog'
    table = 'log'
    delete_cache=False
    @classmethod
    def getAll(cls, where={}, condiciones={}, select=""):
        return_total = None
        connection = database.instance()
        # fields     = table.getByname(cls.table)
        fields = {}

        if 'order' not in condiciones and 'orden' in fields:
            condiciones['order'] = 'fecha DESC'

        if 'palabra' in condiciones:
            condiciones['buscar'] = {}
            if 'tabla' in fields:
                condiciones['buscar']['tabla'] = condiciones['palabra']
            if 'accion' in fields:
                condiciones['buscar']['accion'] = condiciones['palabra']
            if 'administrador' in fields:
                condiciones['buscar']['administrador'] = condiciones['palabra']

            if len(condiciones['buscar']) == 0:
                del condiciones['buscar']

        if select == 'total':
            return_total = True

        row = connection.get(cls.table, cls.idname, where, condiciones, select)
        if return_total != None:
            return len(row)
        else:
            return row

    @classmethod
    def insert(cls, set_query,  loggging=True):
        # fields     = table.getByname(cls.table)
        fields = {}
        insert = database.create_data(fields, set_query)
        connection = database.instance()
        row = connection.insert(cls.table, cls.idname, insert,cls.delete_cache)
        if isinstance(row, int) and row > 0:
            last_id = row
            if loggging:
                #log.insert_log(cls.table, cls.idname, cls, insert)
                pass
            return last_id
        else:
            return row
    @classmethod
    def insert_log(cls,tabla:str, idname:str, funcion:str, row:dict):
        if (tabla != cls.table and !app._front:
            administrador = _SESSION['nombre' . app.prefix_site] . ' (' . _SESSION['email' . app.prefix_site] . ')'

            accion = 'metodo: ' . funcion
            if (isset(row['titulo'])) {
                accion .= ', titulo: ' . row['titulo']
            } elseif (isset(row['nombre'])) {
                accion .= ', nombre: ' . row['nombre']
            } elseif (isset(row['tablename'])) {
                accion .= ', Tabla: ' . row['tablename']
            }
            if (isset(row[idname])) {
                accion .= ', ID: ' . row[idname]
            } elseif (isset(row['id'])) {
                accion .= ', ID: ' . row['id']
            }

            data = array(
                'administrador' => administrador,
                'tabla'         => tabla,
                'accion'        => accion,
                'fecha'         => date('Y-m-d H:i:s'),
            )
            cls.insert(data)
        }
    }