from core.view import view
from .head import head
class lista:
    metadata  = {'title' : ''}

    def __init__(self,metadata:dict):
        for key,value in metadata.items():
            self.metadata[key] = value


    def normal(self,data:dict):
        ret={'body':''}
        th       = data['th']
        row_data = data['row']
        row      = []
        even     = False
        for fila in row_data:
            td = []
            for v in th:
                content = self.field(v, fila)
                td.append({'content' : content, 'content_field' : v['field']})
            
            linea = {'even' : even, 'id' : fila[0], 'td' : td, 'order' : fila['orden'] if 'orden' in fila else ''}
            row.append(linea)
            even  = not even
        
        data['row']         = row
        data['title']       = self.metadata['title']
        data['is_order'] = 'orden' in th

        data = self.pagination(data)

        data['delete'] = 'delete' in th

        h = head(cls.metadata)
        ret_head=h.normal()
        if ret_head['headers']!='':
            return ret_head
        ret['body']+=ret_head['body']

        header = new header()
        header->normal()
        aside = new aside()
        aside->normal()

        view::set_array(data)
        view::render('list')

        footer = new footer()
        footer->normal()
    }