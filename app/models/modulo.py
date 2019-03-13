from core.database import database
from .base_model import base_model
from .log import log
from .table import table
import json


class modulo(base_model):
    idname = 'idmodulo'
    table = 'modulo'
    @classmethod
    def getAll(cls, where={}, condiciones={}, select=""):
        return_total = None
        connection = database.instance()
        fields     = table.getByname(cls.table)

        if 'order' not in condiciones and 'orden' in fields:
            condiciones['order'] = 'orden ASC'

        if 'palabra' in condiciones:
            condiciones['buscar'] = {}
            if 'titulo' in fields:
                condiciones['buscar']['titulo'] = condiciones['palabra']

            if len(condiciones['buscar']) == 0:
                del condiciones['buscar']

        if select == 'total':
            return_total = True

        row = connection.get(cls.table, cls.idname, where, condiciones, select)
        for r in row:
            if 'menu' in r and r['menu']!='':
                r['menu'] = json.loads(r['menu'])
            if 'mostrar' in r and r['mostrar']!='':
                r['mostrar'] = json.loads(r['mostrar'])
            if 'detalle' in r and r['detalle']!='':
                r['detalle'] = json.loads(r['detalle'])
            if 'recortes' in r and r['recortes']!='':
                r['recortes'] = json.loads(r['recortes'])
            else:
                r['recortes']=[]
            
            if 'estado' in r and r['estado']!='':
                r['estado'] = json.loads(r['estado'])

        if return_total != None:
            return len(row)
        else:
            return row

    @classmethod
    def getById(cls, id: int):
        where = {cls.idname: id}
        connection = database.instance()
        row = connection.get(cls.table, cls.idname, where)
        if len(row) == 1:
            row[0]['menu'] = json.loads(row[0]['menu'])
            row[0]['mostrar'] = json.loads(row[0]['mostrar'])
            row[0]['detalle'] = json.loads(row[0]['detalle'])
            if row[0]['recortes']!='':
                row[0]['recortes'] = json.loads(row[0]['recortes'])
            else:
                row[0]['recortes']=[]
            row[0]['estado'] = json.loads(row[0]['estado'])
        return row[0] if len(row) == 1 else row

    @classmethod
    def copy(cls, id: int, loggging=True):
        row = cls.getById(id)
        row['menu'] = json.dumps(row['menu'])
        row['mostrar'] = json.dumps(row['mostrar'])
        row['detalle'] = json.dumps(row['detalle'])
        row['recortes'] = json.dumps(row['recortes'])
        row['estado'] = json.dumps(row['estado'])

        fields     = table.getByname(cls.table)
        insert = database.create_data(fields, row)
        connection = database.instance()
        row = connection.insert(cls.table, cls.idname, insert)
        if isinstance(row, int) and row > 0:
            last_id = row
            if loggging:
                log.insert_log(cls.table, cls.idname, cls, insert)
                pass
            return last_id
        else:
            return row
