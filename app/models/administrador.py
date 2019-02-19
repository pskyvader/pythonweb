from core.database import database
from . import base_model
class administrador(base_model):
    @staticmethod
    def get_all():
        connection = database.instance()
        if connection._errors!='':
            return connection._errors
        else:
            row = connection.consulta('select * from seo_administrador',True)
        return row
