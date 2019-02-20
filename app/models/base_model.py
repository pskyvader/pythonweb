from core.database import database
from core.app import app
import json


class base_model:
    idname = ''
    table = ''

    @classmethod
    def getAll(cls, where={}, condiciones={}, select=""):
        limit = None
        idpadre = None
        return_total = None
        connection = database.instance()
        # fields     = table.getByname(cls.table)
        fields = {}
        if 'estado' not in where and app.front and 'estado' in fields:
            where['estado'] = True

        if 'idpadre' in where:
            if 'idpadre' in fields:
                idpadre = where['idpadre']
                if 'limit' in condiciones:
                    limit = condiciones['limit']
                    limit2 = 0
                    del condiciones['limit']

                if 'limit2' in condiciones:
                    if limit == None:
                        limit = 0
                    limit2 = condiciones['limit2']
                    del condiciones['limit2']
            del where['idpadre']
        

        if 'order' not in condiciones and 'orden' in fields:
            condiciones['order'] = 'orden ASC'

        if 'palabra' in condiciones:
            condiciones['buscar'] = {}
            if 'titulo' in fields:
                condiciones['buscar']['titulo'] = condiciones['palabra']

            if 'keywords' in fields:
                condiciones['buscar']['keywords'] = condiciones['palabra']

            if 'descripcion' in fields:
                condiciones['buscar']['descripcion'] = condiciones['palabra']

            if 'metadescripcion' in fields:
                condiciones['buscar']['metadescripcion'] = condiciones['palabra']

            if 'cookie_pedido' in fields:
                condiciones['buscar']['cookie_pedido'] = condiciones['palabra']

            if len(condiciones['buscar']) == 0:
                del condiciones['buscar']

        if select == 'total':
            return_total = True
            if idpadre != None:
                select = ''

        row = connection.get(cls.table, cls.idname, where, condiciones, select)
        deleted = False
        for r in row:
            deleted = False
            if 'idpadre' in r:
                r['idpadre'] = json.loads(r['idpadre'])
                if idpadre != None and idpadre not in r['idpadre']:
                    deleted = True
                    del r

            if return_total == None:
                if not deleted and 'foto' in r:
                    r['foto'] = json.loads(r['foto'])
                else:
                    print('no foto')

                if not deleted and 'archivo' in r:
                    r['archivo'] = json.loads(r['archivo'])

        if limit != None:
            if limit2 == 0:
                row = row[0:limit]
            else:
                row = row[limit:limit2+1]

        if return_total != None:
            return len(row)
        else:
            return row

    @classmethod
    def getById(cls,id):
        where = {cls.idname : id}
        if app.front:
            # fields     = table.getByname(cls.table)
            fields = {}
            if 'estado' in fields:
                where['estado'] = True
            
        
        connection = database.instance()
        row        = connection.et(cls.table, cls.idname, where)
        if len(row) == 1:
            if 'foto' in row[0]:
                row[0]['foto'] = json.loads(row[0]['foto'])
            if 'archivo' in row[0]:
                row[0]['archivo'] = json.loads(row[0]['archivo'])
        return row[0] if len(row) == 1 else row