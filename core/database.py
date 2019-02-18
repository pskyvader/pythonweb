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
        except expression as identifier:
            throw new \Exception("Error {e.getMessage()}", 1)
            die()
        
    def conect(self):
        self._connection = PyMySQL.connect(self._dbHost,self._dbUser,self._dbPassword,self._dbName )