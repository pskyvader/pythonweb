from core.database import database
class administrador:
    @staticmethod
    def get_all():
        connection = database.instance()
        row = connection.consulta('select * from seo_administrador',False)
        return row
