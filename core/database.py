from core.app import app
import PyMySQL
class database():
    _dbUser=''
    _dbPassword=''
    _dbHost=''
    _dbName=''

    _connection=''
    _instance=''

    _prefix=''

    def __init__(self):
        try:
            config            = app.get_config
            self._dbHost     = config["host"]
            self._dbUser     = config["user"]
            self._dbPassword = config["password"]
            self._dbName     = config["database"]
            self._prefix     = config["prefix"] + "_"
            self.conect()
        except:
            print('error DB')
            return False
        
    def conect(self):
        self._connection = PyMySQL.connect(self._dbHost,self._dbUser,self._dbPassword,self._dbName )

    def prepare(self,sql):
        cursor=self._connection.cursor()
        return cursor
        
    def consulta(self,sql, return_query, delete_cache = True):
        try:
            cursor=self.prepare(sql)
            cursor.execute(sql)
            self._connection.commit()
            if return_query:
                rows = cursor.fetchall()
            #else:
                #if delete_cache:
                    #cache.delete_cache()
        except:
            self._connection.rollback()
            print('error DB query')


        if (!isset(rows)) {
            if (return_query) {
                rows = array()
            } else {
                rows = true
            }
        }

        return rows