from core.app import app
#import PyMySQL
import pymysql


class database():
    _dbUser = ''
    _dbPassword = ''
    _dbHost = ''
    _dbName = ''

    _connection = None
    _instance = None

    _prefix = ''
    _errors = ''

    def __init__(self):
        try:
            config = app.get_config()
            self._dbHost = config["host"]
            self._dbUser = config["user"]
            self._dbPassword = config["password"]
            self._dbName = config["database"]
            self._prefix = config["prefix"] + "_"
            self.conect()
        except:
            print('error DB connection')
            self._errors = 'Error DB connection ' + self._dbHost + ',' + \
                self._dbUser + ','+self._dbPassword + ','+self._dbName

    def conect(self):
        self._connection = pymysql.connect(
            self._dbHost, self._dbUser, self._dbPassword, self._dbName, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    def prepare(self):
        cursor = self._connection.cursor()
        return cursor

    def consulta(self, sql, return_query, delete_cache=True):
        rows = None
        try:
            cursor = self.prepare()
            cursor.execute(sql)
            self._connection.commit()
            if return_query:
                rows = cursor.fetchall()
                for r in rows:
                    for k,v in enumerate(list(r.values())):
                        r[k] = v
            # else:
                # if delete_cache:
                # cache.delete_cache()
        except:
            self._connection.rollback()
            print('error DB query')

        if rows is None:
            if return_query:
                rows = {}
            else:
                rows = True

        return rows

    def get_last_insert_id(self):
        return self._connection.insert_id()
    

    @staticmethod
    def instance():
        if database._instance is None:
            database._instance = database()
        return database._instance
