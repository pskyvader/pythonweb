from core.database import database
from .base_model import base_model
import json

class modulo(base_model):
    idname = 'idmodulo'
    table = 'modulo'
    @classmethod
    def getAll(cls, where={}, condiciones={}, select=""):
        return_total = None
        connection = database.instance()
        # fields     = table.getByname(cls.table)
        fields = {}


        if 'order' not in condiciones and 'orden' in fields:
            condiciones['order'] = 'orden ASC'

        if 'palabra' in condiciones:
            condiciones['buscar'] = {}
            if 'titulo' in fields:
                condiciones['buscar']['titulo'] = condiciones['palabra']

            if len(condiciones['buscar']) == 0:
                del condiciones['buscar']

        if select == 'total':
            return_total = True

        row = connection.get(cls.table, cls.idname, where, condiciones, select)
        deleted = False
        for r in row:
            if 'menu' in r:
                r['menu'] = json.loads(r['menu'])
            

            if 'mostrar' in r:
                r['mostrar'] = json.loads(r['mostrar'])
            

            if 'detalle' in r:
                r['detalle'] = json.loads(r['detalle'])
            

            if 'recortes' in r:
                r['recortes'] = json.loads(r['recortes'])
            

            if 'estado' in r:
                r['estado'] = json.loads(r['estado'])
                

        if return_total != None:
            return len(row)
        else:
            return row


    @classmethod
    def getById(cls, id):
        where = {cls.idname: id}
        if app.front:
            # fields     = table.getByname(cls.table)
            fields = {}
            if 'estado' in fields:
                where['estado'] = True

        connection = database.instance()
        row = connection.get(cls.table, cls.idname, where)
        if len(row) == 1:
            if 'foto' in row[0]:
                row[0]['foto'] = json.loads(row[0]['foto'])
            if 'archivo' in row[0]:
                row[0]['archivo'] = json.loads(row[0]['archivo'])
        return row[0] if len(row) == 1 else row


    public static function getById(int $id)
    {
        $where      = array(static::$idname => $id)
        $connection = database::instance()
        $row        = $connection->get(static::$table, static::$idname, $where)
        if count($row) == 1) {
            $row[0]['menu']     = json.loads($row[0]['menu'])
            $row[0]['mostrar']  = json.loads($row[0]['mostrar'])
            $row[0]['detalle']  = json.loads($row[0]['detalle'])
            $row[0]['recortes'] = json.loads($row[0]['recortes'])
            $row[0]['estado']   = json.loads($row[0]['estado'])
        }
        return (count($row) == 1) ? $row[0] : $row
    }

    public static function copy(int $id)
    {
        $row             = static::getById($id)
        $row['menu']     = functions::encode_json($row['menu'])
        $row['mostrar']  = functions::encode_json($row['mostrar'])
        $row['detalle']  = functions::encode_json($row['detalle'])
        $row['recortes'] = functions::encode_json($row['recortes'])
        $row['estado']   = functions::encode_json($row['estado'])
        $fields          = table::getByname(static::$table)
        $insert          = database::create_data($fields, $row)
        $connection      = database::instance()
        $row             = $connection->insert(static::$table, static::$idname, $insert)
        if is_int($row) && $row>0) {
            $last_id = $row
            if $log) {
                log::insert_log(static::$table, static::$idname, __FUNCTION__, $insert)
            }
            return $last_id
        } else {
            return $row
        }
    }