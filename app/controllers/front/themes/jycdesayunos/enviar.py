from core.app import app
from core.email import email
from core.functions import functions

from .base import base

from email.utils import parseaddr
import urllib.request
import json

class enviar(base):

    def index(self):
        ret = {"body": []}
        ret = {'headers': [ ('Content-Type', 'application/json charset=utf-8')], 'body': ''}
        campos        = app.post['campos']
        respuesta     = {'exito' : True, 'mensaje' : ''}
        nombre_sitio  = app.title
        config        = app.get_config()
        secret        = config['google_captcha_secret']
        email_empresa = config['main_email']

        if campos['nombre']=='':
            respuesta['mensaje'] += '<strong>Error!</strong>&nbsp Nombre vacío.<br/>'

        if campos['email']=='':
            respuesta['mensaje'] += '<strong>Error!</strong>&nbsp Email vacío.<br/>'
        elif '@' not in parseaddr(campos['email'])[1]:        
            respuesta['mensaje'] += '<strong>Error!</strong>&nbsp Email no valido.<br/>'
        
        if campos['mensaje']=='':
            respuesta['mensaje'] += '<strong>Error!</strong>&nbsp Mensaje vacío.<br/>'

        if 'g-recaptcha-response' not in campos or campos['g-recaptcha-response']=='':
            respuesta['mensaje'] += '<strong>Error!</strong>&nbsp Error en captcha. Por favor completa el captcha.<br/>'
            respuesta['captcha']=True
        

        if respuesta['mensaje'] != '':
            respuesta['exito'] = False
        

        if (respuesta['exito']) 
            url                  = 'https://www.google.com/recaptcha/api/siteverify?secret=' + secret + '&response=' + campos['g-recaptcha-response'] + '&remoteip=' + app.client_ip
            
            file = urllib.request.urlopen(url)
            captcha              = json functions.decode_json(file)
            respuesta['exito']   = (captcha['success'])
            if (!respuesta['exito']) 
                respuesta['mensaje'] = '<strong>Error!</strong>&nbsp Error en captcha. Por favor completa el captcha.'
            
            respuesta['captcha']=True
            unset(campos['g-recaptcha-response'])
        

        if (respuesta['exito']) 
            body_email = array(
                'body'     : view.get_theme() . 'mail/contacto.html',
                'titulo'   : "Formulario de " . campos['titulo'],
                'cabecera' : "Estimado " . campos['nombre'] . ", hemos recibido su correo, el cual será respondido a la brevedad por el centro de atención al cliente de " . nombre_sitio,
            )
            titulo                      = campos['titulo']
            body_email['campos_largos'] = array('Mensaje' : nl2br(campos['mensaje']))
            unset(campos['accion'], campos['titulo'], campos['mensaje'])
            body_email['campos'] = campos
            imagenes             = array()

            adjuntos = array()
            if (isset(_FILES)) 
                foreach (_FILES as key : file) 
                    adjuntos[] = array('archivo' : file['tmp_name'], 'nombre' : file['name'])
                
            
            body      = email.body_email(body_email)
            respuesta = email.enviar_email(array(campos['email'], email_empresa), "Formulario de " . titulo, body, adjuntos, imagenes)
            if (respuesta['exito']) 
                respuesta['mensaje'] = "<strong>Gracias!</strong>&nbsp Email enviado correctamente."
                respuesta['captcha']=True
             else 
                respuesta['mensaje'] = "<strong>Error!</strong>&nbsp No se puede enviar el email, por favor intente más tarde.<br/>" . respuesta['mensaje']
                respuesta['captcha']=True
            
        
        echo functions.encode_json(respuesta)
    

