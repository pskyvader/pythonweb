from core.app import app
class database():
    _dbUser
    _dbPassword
    _dbHost
    _dbName

    _connection
    _instance

    _prefix

    def __init__(self):
        try {
            $config            = app.get_config
            $this->_dbHost     = $config["host"];
            $this->_dbUser     = $config["user"];
            $this->_dbPassword = $config["password"];
            $this->_dbName     = $config["database"];
            self::$_prefix     = $config["prefix"] . "_";
            $this->conect();
        } catch (\PDOException $e) {
            throw new \Exception("Error {$e->getMessage()}", 1);
            die();
        }
