from core.database import database
from .base_model import base_model


class administrador(base_model):
    idname = 'idadministrador'
    table = 'administrador'
    cookie = ''

    @classmethod
    def insert(cls, data,  loggging=True):
        if 'pass' in data and data['pass'] != '':
            if 'pass_repetir' in data and data['pass_repetir'] != '':
                if data['pass'] != data['pass_repetir']:
                    return {'exito': False, 'mensaje': 'Contraseñas no coinciden'}
            else:
                return {'exito': False, 'mensaje': 'Contraseña no existe'}
        else:
            return {'exito': False, 'mensaje': 'Contraseña no existe'}

        # fields     = table.getByname(cls.table)
        fields = {}
        insert = database.create_data(fields, data)
        insert['pass'] = database.encript(insert['pass'])
        insert['email'] = insert['email'].lower()

        connection = database.instance()
        row = connection.insert(cls.table, cls.idname, insert)
        if isinstance(row, int) and row > 0:
            last_id = row
            if loggging:
                #log.insert_log(cls.table, cls.idname, cls, insert)
                pass
            return last_id
        else:
            return row
