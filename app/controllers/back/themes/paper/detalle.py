from core.app import app
from core.functions import functions
from core.image import image
from core.view import view
from .head import head
from .header import header
from .aside import aside
from .footer import footer

class detalle:
    metadata   = {'title' : ''}
    max_upload = "Ilimitado"

    def __init__(self,metadata):
        for key, value in metadata.items():
            self.metadata[key] = value



    def normal(self, data: dict):
        ret = {'body': ''}
        campos = data['campos']
        row_data = data['row']
        row = []


        for v in campos:
            content = self.field(v, row_data)
            row.append({'content' : content, 'content_field' : v['field'], 'class' : 'hidden' if 'hidden' == v['type'] else ''})
        


        data['row'] = row
        data['title'] = self.metadata['title']


        h = head(self.metadata)
        ret_head = h.normal()
        if ret_head['headers'] != '':
            return ret_head
        ret['body'] += ret_head['body']

        he = header()
        ret['body'] += he.normal()['body']

        asi = aside()
        ret['body'] += asi.normal()['body']

        view.add_array(data)
        view.render('detail')

        f = footer()
        ret['body'] += f.normal()['body']


