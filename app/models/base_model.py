from core.database import database
class base_model:
    idname = ''
    table                = ''

    @staticmethod
    def getAll(dict where = {}, dict condiciones = {}, str select = ""):
    
        connection = database::instance();
        fields     = table::getByname(static::table);
        if (!isset(where['estado']) && app::_front && isset(fields['estado'])) {
            where['estado'] = true;
        }

        if (isset(where['idpadre'])) {
            idpadre = where['idpadre'];
            unset(where['idpadre']);
            if (isset(condiciones['limit'])) {
                limit  = condiciones['limit'];
                limit2 = 0;
                unset(condiciones['limit']);
            }
            if (isset(condiciones['limit2'])) {
                if (!isset(limit)) {
                    limit = 0;
                }

                limit2 = condiciones['limit2'];
                unset(condiciones['limit2']);
            }
        }

        if (!isset(condiciones['order']) && isset(fields['orden'])) {
            condiciones['order'] = 'orden ASC';
        }

        if (isset(condiciones['palabra'])) {
            condiciones['buscar'] = array();
            if (isset(fields['titulo'])) {
                condiciones['buscar']['titulo'] = condiciones['palabra'];
            }

            if (isset(fields['keywords'])) {
                condiciones['buscar']['keywords'] = condiciones['palabra'];
            }

            if (isset(fields['descripcion'])) {
                condiciones['buscar']['descripcion'] = condiciones['palabra'];
            }

            if (isset(fields['metadescripcion'])) {
                condiciones['buscar']['metadescripcion'] = condiciones['palabra'];
            }
            
            if (isset(fields['cookie_pedido'])) {
                condiciones['buscar']['cookie_pedido'] = condiciones['palabra'];
            }

            if (count(condiciones['buscar']) == 0) {
                unset(condiciones['buscar']);
            }

        }
        if (select == 'total') {
            return_total = true;
            if (isset(idpadre)) {
                select = '';
            }
        }
        row = connection->get(static::table, static::idname, where, condiciones, select);
        foreach (row as key => value) {
            if (isset(row[key]['idpadre'])) {
                row[key]['idpadre'] = functions::decode_json(row[key]['idpadre']);
                if (isset(idpadre) && !in_array(idpadre, row[key]['idpadre'])) {
                    unset(row[key]);
                }
            }
            if (isset(row[key]['foto'])) {
                row[key]['foto'] = functions::decode_json(row[key]['foto']);
            }
            if (isset(row[key]['archivo'])) {
                row[key]['archivo'] = functions::decode_json(row[key]['archivo']);
            }
        }
        if (isset(idpadre)) {
            row = array_values(row);
        }

        if (isset(limit)) {
            if (limit2 == 0) {
                row = array_slice(row, limit2, limit);
            } else {
                row = array_slice(row, limit, limit2);
            }
        }
        if (isset(return_total)) {
            return count(row);
        }
        return row;
    }