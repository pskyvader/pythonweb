from core.app import app
from core.database import database
from .base_model import base_model
from .log import log
import json


class producto(base_model):
    idname = 'idproducto'
    table = 'producto'

    @classmethod
    def getById(cls, id: int):
        where = {cls.idname: id}
        if app.front:
            # fields     = table.getByname(cls.table)
            fields = {}
            if 'estado' in fields:
                where['estado'] = True

        connection = database.instance()
        row = connection.get(cls.table, cls.idname, where)
        if len(row) == 1:
            if 'foto' in row[0]:
                row[0]['foto'] = json.loads(row[0]['foto'])
            if 'archivo' in row[0]:
                row[0]['archivo'] = json.loads(row[0]['archivo'])
            row[0]['idpadre'] = json.loads(row[0]['idpadre'])
        return row[0] if len(row) == 1 else row

    @classmethod
    def copy(cls, id: int, loggging=True):
        from .log import log
        from core.image import image
        row = cls.getById(id)

        if 'foto' in row:
            foto_copy = row['foto']
            del row['foto']
        else:
            foto_copy = None

        if 'archivo' in row:
            del row['archivo']
        row['idpadre'] = json.dumps(row['idpadre'])
        # fields     = table.getByname(cls.table)
        fields = {}
        insert = database.create_data(fields, row)
        connection = database.instance()
        row = connection.insert(cls.table, cls.idname, insert)
        if isinstance(row, int) and row > 0:
            last_id = row
            if foto_copy != None:
                new_fotos = []
                for foto in foto_copy:
                    copiar = image.copy(
                        foto, last_id, foto['folder'], foto['subfolder'], last_id, '')
                    new_fotos.append(copiar['file'][0])
                    image.regenerar(copiar['file'][0])

                update = {'id': last_id, 'foto': json.dumps(new_fotos)}
                cls.update(update)

            if loggging:
                log.insert_log(cls.table, cls.idname, cls, (insert))
                pass
            return last_id
        else:
            return row
