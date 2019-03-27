from .app import app
from .view import view

import smtplib
import os.path as op
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders



class email:
    @staticmethod
    def body_email(body_email):
        config = app.get_config();
        data = {}
        data['dominio'] = config['domain']
        data['email_empresa'] = config['main_email']
        data['email_from'] = config['email_from']
        data['nombre_sitio'] = config['title']
        data['color_primario'] = config['color_primario']
        data['color_secundario'] = config['color_secundario']
        data['logo'] = 'cid:logo'
        data['titulo'] = body_email['titulo']
        data['cabecera'] = body_email['cabecera']
        data['campos']=body_email['campos']
        data['campos_largos']=body_email['campos_largos']
        template = body_email['template']
        body=view.render([(template, data)],True,view.get_theme()+'mail/')
        
        return body

    @staticmethod
    def enviar_email(send_from, send_to, subject, message, files=[],
                server="localhost", port=587, username='', password='',
                use_tls=True):
        """Compose and send email with provided info and attachments.

        Args:
            send_from (str): from name
            send_to (str): to name
            subject (str): message title
            message (str): message body
            files (list[str]): list of file paths to be attached to email
            server (str): mail server host name
            port (int): port number
            username (str): server auth username
            password (str): server auth password
            use_tls (bool): use TLS mode
        """
        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = COMMASPACE.join(send_to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

        msg.attach(MIMEText(message))

        for path in files:
            part = MIMEBase('application', "octet-stream")
            with open(path, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="{}"'.format(op.basename(path)))
            msg.attach(part)

        smtp = smtplib.SMTP(server, port)
        if use_tls:
            smtp.starttls()
        smtp.login(username, password)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.quit()