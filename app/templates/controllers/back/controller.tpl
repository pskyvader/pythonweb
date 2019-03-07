from .base import base
from app.models.{{class}} import {{class}} as {{class}}_model

#from app.models.table import table

#from .detalle import detalle as detalle_class
#from .lista import lista as lista_class
#from .head import head
#from .header import header
#from .aside import aside
#from .footer import footer

#from core.app import app
#from core.functions import functions
#from core.image import image

class {{class}}(base):
    url = ['{{class}}']
    metadata = {'title' : '{{class}}','modulo':'{{class}}'}
    breadcrumb = []
    def __init__(self):
        super().__init__({{class}}_model)