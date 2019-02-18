from core.database import database
class administrador:
    @staticmethod
    def get_all():
        connection = database.instance()
        if connection is str:
            return connection
        else:
            row = connection.consulta('select * from seo_administrador',False)
        return row
