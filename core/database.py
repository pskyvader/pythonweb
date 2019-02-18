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
        return self._connection.cursor()
    def consulta(self,sql, return_query, delete_cache = true):
        try {
            query = this->prepare(sql)
            query->execute()
            if (return_query) {
                rows = query->fetchAll()
            } else {
                if (delete_cache) {
                    cache::delete_cache()
                }
            }

        } catch (\PDOException e) {
            if (error_reporting()) {
                echo "Consulta: " . sql . "<br>"
                print "Error!: " . e->getMessage()
            }
        }

        if (!isset(rows)) {
            if (return_query) {
                rows = array()
            } else {
                rows = true
            }
        }

        return rows