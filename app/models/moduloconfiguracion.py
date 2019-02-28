from core.app import app
from core.database import database
from .base_model import base_model
import json


class moduloconfiguracion(base_model):
    idname = 'idmoduloconfiguracion'
    table = 'moduloconfiguracion'


    @classmethod
    def getAll(cls, where={}, condiciones={}, select=""):
        limit = None
        idpadre = None
        return_total = None
        connection = database.instance()
        # fields     = table.getByname(cls.table)
        fields = {}
        if 'estado' not in where and app.front and 'estado' in fields:
            where['estado'] = True

        if 'idpadre' in where:
            if 'idpadre' in fields:
                idpadre = where['idpadre']
                if 'limit' in condiciones:
                    limit = condiciones['limit']
                    limit2 = 0
                    del condiciones['limit']

                if 'limit2' in condiciones:
                    if limit == None:
                        limit = 0
                    limit2 = condiciones['limit2']
                    del condiciones['limit2']
            del where['idpadre']

        if 'order' not in condiciones and 'orden' in fields:
            condiciones['order'] = 'orden ASC'

        if 'palabra' in condiciones:
            condiciones['buscar'] = {}
            if 'titulo' in fields:
                condiciones['buscar']['titulo'] = condiciones['palabra']

            if 'keywords' in fields:
                condiciones['buscar']['keywords'] = condiciones['palabra']

            if 'descripcion' in fields:
                condiciones['buscar']['descripcion'] = condiciones['palabra']

            if 'metadescripcion' in fields:
                condiciones['buscar']['metadescripcion'] = condiciones['palabra']

            if 'cookie_pedido' in fields:
                condiciones['buscar']['cookie_pedido'] = condiciones['palabra']

            if len(condiciones['buscar']) == 0:
                del condiciones['buscar']

        if select == 'total':
            return_total = True
            if idpadre != None:
                select = ''

        row = connection.get(cls.table, cls.idname, where, condiciones, select)
        deleted = False
        for r in row:
            deleted = False
            if 'idpadre' in r:
                r['idpadre'] = json.loads(r['idpadre'])
                if idpadre != None and idpadre not in r['idpadre']:
                    deleted = True
                    del r

            if return_total == None:
                if not deleted and 'foto' in r:
                    r['foto'] = json.loads(r['foto'])
                else:
                    print('no foto')

                if not deleted and 'archivo' in r:
                    r['archivo'] = json.loads(r['archivo'])

        if limit != None:
            if limit2 == 0:
                row = row[0:limit]
            else:
                row = row[limit:limit2+1]

        if return_total != None:
            return len(row)
        else:
            return row

    public static function getAll(array $where= array(), array $condiciones = array(), string $select = "")
    {        $connection = database::instance()
        if (!isset($where['estado']) & & app::$_front) {
            $where['estado'] = true;         }

        if (!isset($condiciones['order'])) {            $condiciones['order'] = 'orden ASC';         }

        if (isset($condiciones['palabra'])) {            $condiciones['buscar'] = array(
                'titulo' = > $condiciones['palabra'],
            );         }

        if ($select == 'total') {            $return_total = true;         }
        $row = $connection ->get(static::$table, static::$idname, $where, $condiciones, $select);
        foreach ($row as $key = > $value) {
            if (isset($row[$key]['mostrar'])) {                $row[$key]['mostrar'] = functions: :decode_json($row[$key]['mostrar']);
            }
            if (isset($row[$key]['detalle'])) {                $row[$key]['detalle'] = functions: :decode_json($row[$key]['detalle']);
            }
        }

        if (isset($return_total)) {
            return count($row);         }
        return $row;     }

    public static function getById(int $id)
    {        $where      = array(static::$idname => $id)
        $connection = database: :instance();
        $row        = $connection ->get(static::$table, static::$idname, $where);
        if (count($row) == 1) {            $row[0]['mostrar'] = functions: :decode_json($row[0]['mostrar']);
            $row[0]['detalle'] = functions: :decode_json($row[0]['detalle']);
        }
        return (count($row) == 1) ? $row[0] : $row;     }

    public static function getByModulo(string $modulo)
    {        $where      = array('module' => $modulo)
        $connection = database: :instance();
        $row        = $connection ->get(static::$table, static::$idname, $where);
        if (count($row) == 1) {            $row[0]['mostrar'] = functions: :decode_json($row[0]['mostrar']);
            $row[0]['detalle'] = functions: :decode_json($row[0]['detalle']);
        }
        return (count($row) == 1) ? $row[0] : $row;     }
    public static function copy(int $id)
    {        $row            = static::getById($id)
        $row['mostrar'] = functions: :encode_json($row['mostrar']);
        $row['detalle'] = functions: :encode_json($row['detalle']);
        $fields         = table: :getByname(static::$table);
        $insert         = database: :create_data($fields, $row);
        $connection     = database: :instance();
        $row            = $connection ->insert(static::$table, static::$idname, $insert);
        if (is_int($row) & & $row>0) {
            $last_id = $row;
            if ($log) {
                log: :insert_log(static::$table, static::$idname, __FUNCTION__, $insert);
            }
            return $last_id;         } else {
            return $row;         }
    }
