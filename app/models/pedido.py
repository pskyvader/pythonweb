from core.app import app
from core.database import database
from core.functions import functions
from .base_model import base_model
from .log import log
from .table import table
import json


class pedido(base_model):
    idname = 'idpedido'
    table = 'pedido'
    delete_cache = False
    @classmethod
    def insert(cls, set_query: dict,  loggging=True):
        fields     = table.getByname(cls.table)
        if not 'fecha_creacion' in set_query:
            set_query['fecha_creacion'] = functions.current_time()

        insert = database.create_data(fields, set_query)
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

    @classmethod
    def update(cls, set_query: dict, loggging=True):
        where = {cls.idname: set_query['id']}
        del set_query['id']
        connection = database.instance()
        row = connection.update(cls.table, cls.idname,
                                set_query, where, cls.delete_cache)
        if loggging:
            log_register=set_query
            log_register.update(where)
            log.insert_log(cls.table, cls.idname, cls, log_register)
        if isinstance(row, bool) and row:
            row = where[cls.idname]
        return row

    @classmethod
    def delete(cls, id: int):
        where = {cls.idname: id}
        connection = database.instance()
        row = connection.delete(cls.table, cls.idname, where, cls.delete_cache)
        log.insert_log(cls.table, cls.idname, cls, where)
        return row

    @classmethod
    def copy(cls, id: int, loggging=True):
        from core.image import image
        row = cls.getById(id)

        if 'foto' in row:
            foto_copy = row['foto']
            del row['foto']
        else:
            foto_copy = None

        if 'archivo' in row:
            del row['archivo']

        fields     = table.getByname(cls.table)
        insert = database.create_data(fields, row)
        connection = database.instance()
        row = connection.insert(cls.table, cls.idname,
                                insert, cls.delete_cache)
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
                log.insert_log(cls.table, cls.idname, cls, insert)
                pass
            return last_id
        else:
            return row

    @classmethod
    def getByCookie(cls, cookie: str, estado_carro=True):
        where = {"cookie_pedido": cookie}
        if estado_carro:
            where['idpedidoestado'] = 1

        connection = database.instance()
        row = connection.get(cls.table, cls.idname, where)
        return row[0] if len(row) == 1 else row

    @classmethod
    def getByIdusuario(cls, idusuario: int, estado_carro=True):
        where = {"idusuario": idusuario}
        if estado_carro:
            where['idpedidoestado'] = 1
        condition = {'order': cls.idname + ' DESC'}
        connection = database.instance()
        row = connection.get(cls.table, cls.idname, where, condition)
        return row[0] if estado_carro and len(row) > 0 else row
