from core.database import database
from .base_model import base_model
from core.app import app
from core.functions import functions


class administrador(base_model):
    idname = 'idadministrador'
    table = 'administrador'
    cookie = ''

    @classmethod
    def insert(cls, set_query,  loggging=True):
        if 'pass' in set_query and set_query['pass'] != '':
            if 'pass_repetir' in set_query and set_query['pass_repetir'] != '':
                if set_query['pass'] != set_query['pass_repetir']:
                    return {'exito': False, 'mensaje': 'Contraseñas no coinciden'}
            else:
                return {'exito': False, 'mensaje': 'Contraseña no existe'}
        else:
            return {'exito': False, 'mensaje': 'Contraseña no existe'}

        # fields     = table.getByname(cls.table)
        fields = {}
        insert = database.create_data(fields, set_query)
        insert['pass'] = database.encript(insert['pass'])
        insert['email'] = insert['email'].lower()

        connection = database.instance()
        row = connection.insert(cls.table, cls.idname, insert)
        if isinstance(row, int) and row > 0:
            last_id = row
            if loggging:
                #log.insert_log(cls.table, cls.idname, cls, insert)
                pass
            return last_id
        else:
            return row

    @classmethod
    def update(cls, set_query, loggging=True):

        if 'id' not in set_query or set_query['id'] == '' or set_query['id'] == 0:
            print('Error, ID perdida')
            return False

        if 'pass' in set_query and set_query['pass'] != '':
            if 'pass_repetir' in set_query and set_query['pass_repetir'] != '':
                if set_query['pass'] != set_query['pass_repetir']:
                    return {'exito': False, 'mensaje': 'Contraseñas no coinciden'}
                else:
                    set_query['pass'] = database.encript(set_query['pass'])
                    set_query['cookie'] = ''
                    del set_query['pass_repetir']

            else:
                return {'exito': False, 'mensaje': 'Contraseña no existe'}

        else:
            del set_query['pass'], set_query['pass_repetir']

        if 'email' in set_query:
            set_query['email'] = set_query['email'].lower()

        where = {cls.idname: set_query['id']}
        del set_query['id']
        connection = database.instance()
        row = connection.update(cls.table, cls.idname, set_query, where)
        if loggging:
            #log.insert_log(cls.table, cls.idname, cls, (set_query+where))
            pass
        if isinstance(row, bool) and row:
            row = where[cls.idname]
        return row

    @staticmethod
    def login_cookie(cookie):
        prefix_site = app.prefix_site
        where       = {'cookie' : cookie}
        condiciones = {'limit' : 1}
        row         = administrador.getAll(where, condiciones)

        if len(row) == 1:
            admin = row[0]
            if admin['estado']:
                profile = profile.getByTipo(admin['tipo'])
                if 'tipo' in profile and profile['tipo']>0:
                    session=app.session
                    session[administrador.idname + prefix_site] = admin[0]
                    session["email" + prefix_site]         = admin['email']
                    session["nombre" + prefix_site]        = admin['nombre']
                    session["estado" + prefix_site]        = admin['estado']
                    session["tipo" + prefix_site]          = admin['tipo']
                    session['prefix_site']                  = prefix_site
                    session.save()
                    #log.insert_log(administrador.table, administrador.idname, administrador, admin)
                    return True
        functions.set_cookie(cookie, 'aaa', (31536000))
        return False