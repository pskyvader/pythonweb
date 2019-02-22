from .app import app
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
            sql += value if (value == "true" or value ==
                             "false") else "'" + str(value).replace("'", "\\'") + "'"

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

    def update(self, table, idname, set_query, where, delete_cache=True):
        set_query = self.process_multiple(set_query)
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
            count += 1
            sql += key + "="
            sql += value if (value == "true" or value ==
                             "false") else "'" + str(value).replace("'", "\\'") + "'"
            sql += ", " if (count < len(set_query)) else ""

        sql += " WHERE (TRUE"
        for key, value in where.items():
            sql += " AND " + key + "='" + str(value) + "'"
        sql += ") "

        if len(where) > 0:
            row = self.consulta(sql, False, delete_cache)
            if (row):
                if len(image) > 0:
                    self.process_image(image, table, idname, where[idname])

                if len(file) > 0:
                    self.process_file(file, table, idname, where[idname])

            return row
        else:
            print("error cantidad de condiciones")
            return False

    def delete(self, table, idname, where, delete_cache=True):
        from core.image import image
        from core.file import file
        sql = "DELETE FROM " + self._prefix + table

        sql += " WHERE (TRUE"
        for key, value in where.items():
            sql += " AND " + key + "='" + str(value) + "'"
        sql += ") "

        if len(where) > 0:
            row = self.consulta(sql, False, delete_cache)
            image.delete(table, '', where[idname])
            file.delete(table, '', where[idname])
            return row
        else:
            print("error cantidad de condiciones")
            return False

    def modify(self, table, column, type_var):
        sql = "ALTER TABLE " + self._prefix + table
        sql += " MODIFY " + column + " " + type_var + " NOT NULL "
        if type_var == 'tinyint(1)':
            sql += " DEFAULT '1' "

        row = self.consulta(sql, False)
        return row

    def add(self, table, column, type_var, after='', primary=False):
        sql = "ALTER TABLE " + self._prefix + table
        sql += " ADD " + column + " " + type_var + " NOT NULL "
        if type_var == 'tinyint(1)':
            sql += " DEFAULT '1' "

        if primary:
            sql += " AUTO_INCREMENT "

        if after != '':
            sql += " AFTER " + after
        else:
            sql += " FIRST"

        if primary:
            sql += ", ADD PRIMARY KEY ('" + column + "')"

        row = self.consulta(sql, False)
        return row

    def create(self, table, columns):
        sql = "CREATE TABLE " + self._prefix + table + " ("
        for key, column in columns.items():
            if key > 0:
                sql += ","

            sql += column['titulo'] + " " + column['tipo'] + " NOT NULL "

            if column['tipo'] == 'tinyint(1)':
                sql += " DEFAULT '1' "

            if column['primary']:
                sql += " AUTO_INCREMENT PRIMARY KEY "

        sql += " )"
        row = self.consulta(sql, False)
        return row

    def truncate(self, tables):
        sql = ""
        for table in tables:
            sql += "TRUNCATE TABLE " + self._prefix + table + " "

        row = self.consulta(sql, False)
        return row

    def restore_backup(self, backup):
        import os
        sql = open(backup, "r").read()
        exito = self.consulta(sql, False)
        if exito:
            os.remove(backup)
        return exito

    def backup(self, tables='*'):
        respuesta = {'exito': False,
                     'mensaje': 'Error al respaldar base de datos', 'sql': []}
        self.disableForeignKeyChecks = True
        self.batchSize = 1000
        try:
            if tables == '*':
                tables = []
                row = self.consulta('SHOW TABLES', True)
                for value in row:
                    tables.append(value[0])
            else:
                tables = tables if isinstance(tables, list) else (
                    tables.replace(' ', '')).split(',')

            sql = ""

            if self.disableForeignKeyChecks == True:
                sql += "SET foreign_key_checks = 0\n\n"

            for table in tables:
                sql += 'DROP TABLE IF EXISTS `' + table + '`'
                row = self.consulta('SHOW CREATE TABLE `' + table + '`', True)
                sql += "\n\n" + row[0][1] + "\n\n"

                row = self.consulta(
                    'SELECT COUNT(*) FROM `' + table + '`', True)
                numRows = row[0][0]

                numBatches = int(numRows / self.batchSize) + 1

                campos = self.consulta("SELECT COLUMN_NAME,COLUMN_TYPE FROM information_schema.columns WHERE table_schema='" +
                                       self._dbName + "' AND table_name='" + table + "'", True)

                for b in range(numBatches+1):
                    query = 'SELECT * FROM `' + table + '` LIMIT ' + \
                        (b * self.batchSize - self.batchSize) + \
                        ',' + self.batchSize
                    row = self.consulta(query, True)
                    realBatchSize = len(row)
                    numFields = len(campos)
                    if realBatchSize != 0:
                        sql += 'INSERT INTO `' + table + '` VALUES '
                        for key, fila in row.items():
                            rowCount = key + 1
                            sql += '('

                            for k, v in campos.items():
                                j = v[0]
                                if j in fila:
                                    fila[j] = self._connection.escape_string(
                                        fila[j])
                                    fila[j] = fila[j].replace("\n", "\\n")
                                    fila[j] = fila[j].replace("\r", "\\r")
                                    fila[j] = fila[j].replace("\f", "\\f")
                                    fila[j] = fila[j].replace("\t", "\\t")
                                    fila[j] = fila[j].replace("\v", "\\v")
                                    fila[j] = fila[j].replace("\a", "\\a")
                                    fila[j] = fila[j].replace("\b", "\\b")
                                    sql += '"' + fila[j] + '"'
                                else:
                                    sql += 'NULL'

                                if k < (numFields - 1):
                                    sql += ','
                            if rowCount == realBatchSize:
                                rowCount = 0
                                sql += ")\n"
                            else:
                                sql += "),\n"

                            rowCount += 1

                    respuesta['sql'].append(sql)
                    sql = ''

                sql += "\n\n"

            if self.disableForeignKeyChecks:
                sql += "SET foreign_key_checks = 1\n"

            respuesta['sql'].append(sql)
            respuesta['exito'] = True
        except Exception as e:
            respuesta['mensaje'] = e

        return respuesta

    @staticmethod
    def encript(password):
        import hashlib
        part1 = hashlib.sha256()
        part1.update(password.encode('utf-8'))
        part2=hashlib.sha256()
        part2.update(part1.hexdigest().encode('utf-8'))
        password= part1.hexdigest() + part2.hexdigest()
        print(password,len(password))
        return password

    @staticmethod
    def create_data(model, data):
        data = database.process_multiple(data)
        m = {}
        for key, value in model.items():
            if key in data:
                m[key] = data[key]
            else:
                if value['tipo'] == 'tinyint(1)':
                    m[key] = 'true'
                else:
                    m[key] = ''
        if 'image' in data:
            m['image'] = data['image']

        if 'file' in data:
            m['file'] = data['file']
        return m

    @staticmethod
    def process_multiple(data):
        import json
        if 'multiple' in data:
            for key, multiple in data['multiple'].items():
                row = {}
                for k, e in multiple.items():
                    if isinstance(e, list):
                        for a, f in e.items():
                            if key == "image" or key == "file":
                                for ke, va in f.items():
                                    row[k][ke][a] = va
                            else:
                                row[a][k] = f
                    else:
                        row[k] = e

                if key != "image" and key != "file":
                    data[key] = json.dumps(row)
                else:
                    data[key] = row
            del data['multiple']
        return data

    def process_image(self, image_list, table, idname, id_image):
        import json
        from core.image import image
        data = {}
        ids = {}
        for key, img in image_list.items():
            row = {}
            portada = False
            for k, f in img.items():
                if 'tmp' in f and f['tmp'] != '':
                    f = image.move(f, table, key, id_image)

                ids[key][f['id']] = f['url']
                if f['portada'] == 'true':
                    if portada:
                        f['portada'] = 'false'
                    else:
                        portada = True
                f['parent'] = id_image
                f['folder'] = table
                row[k] = f

            if not portada:
                row[0]['portada'] = 'true'
            data[key] = json.dumps(row)

        row = self.get(table, idname, {'idname': id_image}, {'limit': 1})
        self.update(table, idname, data, {'idname': id_image})
        for key, value in ids.items():
            images = json.loads(row[0][key])
            if isinstance(images, list):
                for img in images:
                    if img['id'] in value or value[img['id']] != img['url']:
                        image.delete(table, img, id_image, key)

        image.delete_temp()
        return data

    def process_file(self, file_list, table, idname, id_file):
        import json
        from core.file import file
        data = {}
        ids = {}
        for key, archivo in file_list.items():
            row = {}
            for k, f in archivo.items():
                if 'tmp' in f and f['tmp'] != '':
                    f = file.move(f, table, key, id_file)

                ids[key][f['id']] = f['url']
                f['parent'] = id_file
                f['folder'] = table
                row[k] = f

            data[key] = json.dumps(row)

        row = self.get(table, idname, {'idname': id_file}, {'limit': 1})
        self.update(table, idname, data, {'idname': id_file})
        for key, value in ids.items():
            files = json.loads(row[0][key])
            if isinstance(files, list):
                for fi in files:
                    if fi['id'] in value or value[fi['id']] != fi['url']:
                        file.delete(table, fi, id_file, key)

        file.delete_temp()
        return data

    @staticmethod
    def set_prefix(prefix):
        database._prefix = prefix

    @staticmethod
    def get_prefix():
        return database._prefix

    @staticmethod
    def instance():
        if database._instance is None:
            database._instance = database()
        return database._instance
