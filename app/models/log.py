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

