from core.app import app
from core.functions import functions
from core.view import view
from .head import head
from .header import header
from .aside import aside
from .footer import footer


class lista:
    metadata = {'title': ''}

    def __init__(self, metadata: dict):
        for key, value in metadata.items():
            self.metadata[key] = value

    def normal(self, data: dict):
        ret = {'body': ''}
        th = data['th']
        row_data = data['row']
        row = []
        even = False
        for fila in row_data:
            td = []
            for v in th:
                content = self.field(v, fila)
                td.append({'content': content, 'content_field': v['field']})

            linea = {'even': even, 'id': fila[0], 'td': td,
                     'order': fila['orden'] if 'orden' in fila else ''}
            row.append(linea)
            even = not even

        data['row'] = row
        data['title'] = self.metadata['title']
        data['is_order'] = 'orden' in th

        data = self.pagination(data)

        data['delete'] = 'delete' in th

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
        view.render('list')

        f = footer()
        ret['body'] += f.normal()['body']

    def get_row(self, class_name, where: dict, condiciones: dict, urledit: str):
        get = app.get
        limit = int(get['limit']) if 'limit' in get else 10
        page = int(get['page']) if 'page' in get else 1
        search = str(get['search']) if 'search' in get else ''

        if search != '':
            condiciones['palabra'] = search

        count = class_name.getAll(where, condiciones, 'total')
        total = int(count / limit)
        if total < (count / limit):
            total += 1

        condiciones['limit'] = limit
        if page > 1:
            condiciones['limit'] = ((page - 1) * limit)
            condiciones['limit2'] = (limit)

        inicio = (limit * (page - 1)) + 1
        fin = (limit * (page))
        if fin > count:
            fin = count

        row = class_name.getAll(where, condiciones)
        for v in row:
            urltmp = urledit
            urltmp.append(v[0])
            v['url_detalle'] = functions.generar_url(urltmp)

        return {'row': row, 'page': page, 'total': total, 'limit': limit, 'search': search, 'count': count, 'inicio': inicio, 'fin': fin}

    def pagination(self,data: dict):
        import urllib.parse
        get = app.get
        limits = {
            10: {'value': 10, 'text': 10, 'active': ''},
            25: {'value': 25, 'text': 25, 'active': ''},
            100: {'value': 100, 'text': 100, 'active': ''},
            500: {'value': 500, 'text': 500, 'active': ''},
            1000: {'value': 1000, 'text': 1000, 'active': ''},
            1000000: {'value': 1000000, 'text': 'Todos', 'active': ''},
        }
        if data['limit'] in limits:
            limits[data['limit']]['active'] = 'selected'

        data['limits'] = limits

        pagination = []
        rango = 5
        min = 1
        max = data['total']
        sw = False
        while ((max - min) + 1) > rango:
            if sw:
                if min != data['page'] and min + 1 != data['page']:
                    min += 1

            else:
                if max != data['page'] and max - 1 != data['page']:
                    max -= 1

            sw = not sw

        get['page'] = data['page'] - 1
        pagination.append({
            'class_page': 'previous ' + ('' if data['page'] > 1 else 'disabled'),
            'url_page': "?" + urllib.parse.urlencode(get),
            'text_page': '<i class="fa fa-angle-left"> </i> Anterior',
        })

        for i in range(min, max+1):
            get['page'] = i
            pagination.append({
                'class_page': 'active' if data['page'] == i else '',
                'url_page': "?" + urllib.parse.urlencode(get),
                'text_page': i,
            })

        get['page'] = data['page'] + 1
        pagination.append({
            'class_page': 'next ' + ('' if data['page'] < data['total'] else 'disabled'),
            'url_page': "?" + urllib.parse.urlencode(get),
            'text_page': 'Siguiente <i class="fa fa-angle-right"> </i> ',
        })

        data['pagination'] = pagination
        return data

    def field(self,th:dict, fila:dict):

        opts={
            'active': lambda: if 1==1: return 'a'
        }
        if (th['type']=='active'):

        switch ($th['type']) {
            case 'active':
                $data = array(
                    'field'  => $th['field'],
                    'active' => $fila[$th['field']],
                    'id'     => $fila[0],
                    'class'  => ($fila[$th['field']]) ? 'btn-success' : 'btn-danger',
                    'icon'   => ($fila[$th['field']]) ? 'fa-check' : 'fa-close',
                );
                break;
            case 'color':
                if (is_array($fila[$th['field']])) {
                    $data = $fila[$th['field']];
                } else {
                    $data = array('background' => $fila[$th['field']], 'text' => '', 'color' => functions::getContrastColor($fila[$th['field']]));
                }
                break;
            case 'delete':
                $data = array('id' => $fila[0]);
                break;
            case 'link':
                $data = array('text' => $th['title_th'], 'url' => $fila[$th['field']]);
                break;
            case 'image':
                if (isset($fila[$th['field']]) && is_array($fila[$th['field']]) && count($fila[$th['field']]) > 0) {
                    $portada      = image::portada($fila[$th['field']]);
                    $thumb_url    = image::generar_url($portada, 'thumb');
                    $zoom_url     = image::generar_url($portada, 'zoom');
                    $original_url = image::generar_url($portada, '');
                } else {
                    $thumb_url = $zoom_url = $original_url = '';
                }
                $data = array('title' => $th['title_th'], 'url' => $thumb_url, 'zoom' => $zoom_url, 'original' => $original_url, 'id' => $fila[0]);
                break;
            case 'action':
                $data = array(
                    'text'    => $th['title_th'],
                    'id'      => $fila[$th['field']],
                    'action'  => $th['action'],
                    'mensaje' => $th['mensaje'],
                );
                break;
            case 'text':
            default:
                return $fila[$th['field']];
                break;
        }

        view::set_array($data);
        $content=view::render('list/'.$th['type'], false, true);
        return $content;
    }