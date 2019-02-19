from core.database import database
from core.app import app
import json


class base_model:
    idname = ''
    table = ''

    @classmethod
    def getAll(cls,where={}, condiciones={}, select=""):
        limit = None
        idpadre = None
        return_total = None
        connection = database.instance()
        # fields     = table.getByname(cls.table)
        fields = {}
        if 'estado' not in where and app.front and 'estado' in fields:
            where['estado'] = True

        if 'idpadre' in where:
            idpadre = where['idpadre']
            del where['idpadre']
            if 'limit' in condiciones:
                limit = condiciones['limit']
                limit2 = 0
                del condiciones['limit']

            if 'limit2' in condiciones:
                if limit == None:
                    limit = 0
                limit2 = condiciones['limit2']
                del condiciones['limit2']

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
        print(row[0])
        for key,value in enumerate(row):
            if 'idpadre' in row[key]:
                row[key]['idpadre'] = json.loads(row[key]['idpadre'])
                if idpadre!=None and idpadre not in row[key]['idpadre']:
                    del row[key]

            if return_total==None:
                if key in row:
                    print('key in row')
                if key in row and 'foto' in row[key]:
                    row[key]['foto'] = json.loads(row[key]['foto'])
                else:
                    print('no foto')

                if key in row and 'archivo' in row[key]:
                    row[key]['archivo'] = json.loads( row[key]['archivo'])
        
        print(row[0])
        if limit!=None:
            if limit2 == 0:
                row=row[0:limit]
            else:
                row=row[limit:limit2]

        if return_total!=None:
            return len(row)
        else:
            return row
