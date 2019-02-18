from core.database import database
class administrador:
    @staticmethod
    def get_all():
        connection = database.instance()
        row = connection.consultaget('select * from seo_administrador')
        return row
