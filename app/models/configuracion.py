from core.database import database
from .base_model import base_model


class configuracion(base_model):
    idname = 'idconfiguracion'
    table = 'configuracion'

    @classmethod
    def getByVariable(cls, variable: str):
        where = {'variable': variable}
        condicion = {'limit': 1}
        connection = database.instance()
        row = connection.get(cls.table, cls.idname, where, condicion)
        return row[0]['valor'] if (len(row) == 1) else False

    @classmethod
    def setByVariable(cls, variable: str, valor: str):
        where = {'variable': variable}
        condicion = {'limit': 1}
        connection = database.instance()
        row = connection.get(cls.table, cls.idname, where, condicion)

        if len(row) == 0:
            row = cls.insert({'variable': variable, 'valor': valor})
        else:
            row = cls.update(
                {'variable': variable, 'valor': valor, 'id': row[0][0]})

        return row
