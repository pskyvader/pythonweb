

from .base import base
from app.models.configuracionadministrador import configuracionadministrador as configuracionadministrador_model

#from app.models.table import table
#from app.models.administrador import administrador as administrador_model

#from .detalle import detalle as detalle_class
#from .lista import lista as lista_class
#from .head import head
#from .header import header
#from .aside import aside
#from .footer import footer

#from core.app import app
#from core.functions import functions
#from core.image import image

class configuracionadministrador(base):
    url = ['configuracionadministrador']
    metadata = {'title' : 'configuracionadministrador','modulo':'configuracionadministrador'}
    breadcrumb = []
    def __init__(self):
        super().__init__(configuracionadministrador_model)