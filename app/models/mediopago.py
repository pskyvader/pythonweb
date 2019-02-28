from .base_model import base_model


class mediopago(base_model):
    idname = 'idmediopago'
    table = 'mediopago'
    @classmethod
    def getById(cls,id:int):
        where = {cls.idname : id}
        connection = database.instance();
        row        = connection->get(cls.table, cls.idname, where);
        return (count(row) == 1) ? row[0] : row;
    }