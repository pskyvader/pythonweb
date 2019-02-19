from core.app import app
# import PyMySQL
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
                    for k, v in enumerate(list(r.values())):
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

    def get(self, table, idname, where, condiciones={}, select=""):
        if select == "":
            select = "*"
        elif select == 'total':
            select = idname

        sql = "SELECT " + select + " FROM " + self._prefix + table
        sql += " WHERE (TRUE"
        for key, value in where.items():
            sql += " AND " + key + "='" + str(value) + "'"
        sql += ") "

        if 'buscar' in condiciones and isinstance(condiciones['buscar'], dict):
            sql += " AND ("
            count = 0
            for key, value in condiciones['buscar']:
                count += 1
                sql += key + " LIKE '%" + value + "%'"
                sql += " OR " if (count < len(condiciones['buscar'])) else ""
            sql += ") "

        if 'order' in condiciones:
            sql += " ORDER BY " + condiciones['order']

        if 'group' in condiciones:
            sql += " GROUP BY " + condiciones['group']

        if 'limit' in condiciones:
            sql += " LIMIT " + str(condiciones['limit'])
            if 'limit2' in condiciones and condiciones['limit2'] > 0:
                sql += " , " + str(condiciones['limit2'])
        row = self.consulta(sql, True)
        return row

    def insert(self, table, idname, insert, delete_cache=True):
        valor_primario = ""
        image = []
        if 'image' in insert:
            image = insert['image']
            del insert['image']

        file = []
        if 'file' in insert:
            file = insert['file']
            del insert['file']

        sql = "INSERT INTO " + self._prefix + table
        sql += "(" + idname

        for key, value in insert.items():
            sql += "," + key

        sql += ") VALUES ('" + valor_primario + "'"

        for key, value in insert.items():
            sql += ","
            sql += value if (value == "true" or value == "false") else "'" + str(value).replace("'", "\\'") + "'"

        sql += ")"
        row = self.consulta(sql, False, delete_cache)
        if (row):
            last_id = self.get_last_insert_id()
            if len(image) > 0:
                self.process_image(image, table, idname, last_id)
            if len(file) > 0:
                self.process_file(file, table, idname, last_id)
            return last_id
        else: 
            return row
            
    def update(self, table, idname, set_query, where, delete_cache = True):
        set_query   = self.process_multiple(set_query)
        image = []
        if 'image' in set_query:
            image = set_query['image']
            del set_query['image']

        file = []
        if 'file' in set_query:
            file = set_query['file']
            del set_query['file']
        if '...' in set_query:
            del set_query['...']
        
        sql = "UPDATE " + self._prefix + table
        sql += " SET "
        count = 0
        for key, value in set_query.items():
            count+=1
            sql += key + "="
            sql += value if (value == "true" or value == "false") else "'" + str(value).replace("'", "\\'") + "'"
            sql += ", " if (count < len(set_query)) else ""

            
        sql += " WHERE (TRUE"
        foreach (where as key => value) {
            sql += " AND " + key + "='" + value + "'"
        }
        sql += ") "
        if (count(where) > 0) {
            row = this->consulta(sql, false, delete_cache)
            if (row) {
                if (count(image) > 0) {
                    this->process_image(image, table, idname, where[idname])
                }
                if (count(file) > 0) {
                    this->process_file(file, table, idname, where[idname])
                }
            }
            return row
        } else {
            echo "error cantidad de condiciones"
            return false
        }
    }


    @staticmethod
    def instance():
        if database._instance is None:
            database._instance = database()
        return database._instance
