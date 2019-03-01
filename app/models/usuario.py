from core.database import database
from .base_model import base_model
from .log import log
from .table import table
from .profile import profile as profile_model
from core.app import app
from core.functions import functions


class usuario(base_model):
    idname = 'idusuario'
    table = 'usuario'

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

        fields     = table.getByname(cls.table)
        insert = database.create_data(fields, set_query)
        insert['pass'] = database.encript(insert['pass'])
        insert['email'] = insert['email'].lower()

        connection = database.instance()
        row = connection.insert(cls.table, cls.idname, insert)
        if isinstance(row, int) and row > 0:
            last_id = row
            if loggging:
                log.insert_log(cls.table, cls.idname, cls, insert)
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
            if 'pass' in set_query:
                del set_query['pass']
            if 'pass_repetir' in set_query:
                del set_query['pass_repetir']

        if 'email' in set_query:
            set_query['email'] = set_query['email'].lower()

        where = {cls.idname: set_query['id']}
        del set_query['id']
        connection = database.instance()
        row = connection.update(cls.table, cls.idname, set_query, where)
        if loggging:
            log.insert_log(cls.table, cls.idname, cls, (set_query+where))
            pass
        if isinstance(row, bool) and row:
            row = where[cls.idname]
        return row

    @clsmethod
    def login_cookie(cookie):
        prefix_site = app.prefix_site
        where = {'cookie': cookie}
        condiciones = {'limit': 1}
        row = usuario.getAll(where, condiciones)

        if len(row) == 1:
            usuario = row[0]
            if usuario['estado']:
                profile = profile_model.getByTipo(usuario['tipo'])
                if 'tipo' in profile and int(profile['tipo']) > 0:
                    session = app.session
                    session[usuario.idname + prefix_site] = usuario[0]
                    session["emailusuario" + prefix_site] = usuario['email']
                    session["nombreusuario" + prefix_site] = usuario['nombre']
                    session["estadousuario" + prefix_site] = usuario['estado']
                    session["tipousuario" + prefix_site] = usuario['tipo']
                    log.insert_log(usuario.table, usuario.idname, usuario, usuario)
                    return True
        functions.set_cookie(cookie, 'aaa', (31536000))
        return False

    @clsmethod
    def login(email, password, recordar):
        prefix_site = app.prefix_site
        if email == '' or password == '':
            return False

        where = {'email': email.lower(), 'pass': database.encript(password)}
        condiciones = {'limit': 1}
        row = usuario.getAll(where, condiciones)

        if len(row) != 1:
            return False
        else:
            usuario = row[0]
            if not usuario['estado']:
                return False
            else:
                profile = profile_model.getByTipo(usuario['tipo'])
                if not 'tipo' in profile or int(profile['tipo']) <= 0:
                    return False
                else:
                    session = app.session
                    session[usuario.idname + prefix_site] = usuario[0]
                    session["emailusuario" + prefix_site] = usuario['email']
                    session["nombreusuario" + prefix_site] = usuario['nombre']
                    session["estadousuario" + prefix_site] = usuario['estado']
                    session["tipousuario" + prefix_site] = usuario['tipo']
                    log.insert_log(usuario.table, usuario.idname, usuario, usuario)
                    if recordar == 'on':
                        return usuario.update_cookie(usuario[0])
                    else:
                        return True


    @classmethod
    def registro(cls,nombre:str, telefono:str, email:str, password:str, password_repetir:str):
        respuesta = {'exito' : False, 'mensaje' : ''}
        if nombre == "" or email == "" or password == "" or password_repetir == "":
            respuesta['mensaje'] = "Todos los datos son obligatorios"
            return respuesta
        

        where = {
            'email' : email.lower(),
        }
        condiciones = {'limit' : 1}
        row         = cls.getAll(where, condiciones)

        if len(row) > 0:
            respuesta['mensaje'] = "Este email ya existe. Puede recuperar la contraseña en el boton correspondiente"
        else:
            data = {'nombre' : nombre, 'telefono' : telefono, 'email' : email, 'pass' : password, 'pass_repetir' : password_repetir, 'tipo' : 1, 'estado' : True}
            id   = cls.insert(data)
            if not isinstance(id,list):
                respuesta['exito'] = True
            else:
                respuesta = id
                
        return respuesta
    
    @classmethod
    def actualizar(cls,datos:dict):
        respuesta = {'exito' : False, 'mensaje' : ''}
        if datos['nombre'] == "" or datos['telefono'] == "" or datos['email'] == "":
            respuesta['mensaje'] = "Todos los datos son obligatorios"
            return respuesta
        
        usuario     = cls.getById(app.session[cls.idname . app.prefix_site])

        if usuario['email'] != datos['email']:
            where = array(
                'email' : strtolower(datos['email']),
            )
            condiciones = array('limit' : 1)
            row         = cls.getAll(where, condiciones)
            if len(row) > 0:
                respuesta['mensaje'] = "Este email ya existe. No puedes modificar tu email."
                return respuesta
            else:
                respuesta['redirect'] = True
            }
        }
        datos['id'] = usuario[0]
        id          = cls.update(datos)
        if isset(id['exito']):
            respuesta = id
        else:
            respuesta['exito'] = True
        }
        return respuesta
    }



    @clsmethod
    def update_cookie(id_cookie):
        import uuid
        cookie = uuid.uuid4().hex
        data = {'id': id_cookie, 'cookie': cookie}
        exito = usuario.update(data)
        if exito:
            functions.set_cookie('cookieusuario' + app.prefix_site, cookie, (31536000))

        return exito

    @clsmethod
    def logout():
        prefix_site = app.prefix_site
        session = app.session
        del session[usuario.idname + prefix_site]
        del session["email" + prefix_site]
        del session["nombre" + prefix_site]
        del session["estado" + prefix_site]
        del session["tipo" + prefix_site]
        functions.set_cookie('cookieusuario' + prefix_site, 'aaa', (31536000))

    @clsmethod
    def verificar_sesion():
        prefix_site = app.prefix_site
        session = app.session
        if usuario.idname+prefix_site) in session and session[usuario.idname + prefix_site] != '':
            usuario = usuario.getById(
                session[usuario.idname + prefix_site])
            if 0 in usuario and usuario[0] != session[usuario.idname + prefix_site]:
                return False
            elif usuario['email'] != session["email" + prefix_site]:
                return False
            elif usuario['estado'] != session["estado" + prefix_site] or not session["estado" + prefix_site]:
                return False
            elif usuario['tipo'] != session["tipo" + prefix_site] or not session["tipo" + prefix_site]:
                return False
            else:
                profile = profile_model.getByTipo(usuario['tipo'])
                if not 'tipo' in profile or int(profile['tipo']) <= 0:
                    return False
                else:
                    return True

        cookie = functions.get_cookie()
        if 'cookieusuario' + prefix_site) in cookie and cookie['cookieusuario' + prefix_site] != '' and cookie['cookieusuario' + prefix_site] != 'aaa':
            return usuario.login_cookie(cookie['cookieusuario' + prefix_site])

        return False

    @clsmethod
    def recuperar(email):
        """recuperar contraseña"""
        from core.view import view
        nombre_sitio = app.title
        if email == '':
            return False

        where = {'email': email.lower()}
        condiciones = {'limit': 1}
        row = usuario.getAll(where, condiciones)

        if len(row) != 1:
            return False
        else:
            usuario = row[0]
            if not usuario['estado']:
                return False
            else:
                password = functions.generar_pass()
                data = {'id': usuario[0], 'pass': password,
                        'pass_repetir': password}
                row = usuario.update(data)

                if row:
                    body_email = {
                        'body': view.get_theme() + 'mail/recuperar_password.html',
                        'titulo': "Recuperación de contraseña",
                        'cabecera': "Estimado " + usuario["nombre"] + ", se ha solicitado la recuperación de contraseña en " + nombre_sitio,
                        'campos': {'Contraseña (sin espacios)': password},
                        'campos_largos': {},
                    }
                    body = email.body_email(body_email)
                    respuesta = email.enviar_email(
                        [email], 'Recuperación de contraseña', body)

                    log.insert_log(usuario.table, usuario.idname, usuario, usuario)
                    return respuesta
                else:
                    return False
