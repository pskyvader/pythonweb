from core.app import app
from core.database import database
from .base_model import base_model
import json
import datetime


class pedido(base_model):
    idname = 'idpedido'
    table = 'pedido'
    delete_cache = False
    @classmethod
    def insert(cls, set_query: dict,  loggging=True):
        # fields     = table.getByname(cls.table)
        fields = {}
        if not 'fecha_creacion' in set_query:
            set_query['fecha_creacion'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        insert = database.create_data(fields, set_query)
        connection = database.instance()
        row = connection.insert(cls.table, cls.idname, insert)
        if isinstance(row, int) and row > 0:
            last_id = row
            if loggging:
                #log.insert_log(cls.table, cls.idname, cls, insert)
                pass
            return last_id
        else:
            return row



    @classmethod
    def update(cls, set_query: dict, loggging=True):
        where = {cls.idname: set_query['id']}
        del set_query['id']
        connection = database.instance()
        row = connection.update(cls.table, cls.idname, set_query, where,)
        if loggging:
            #log.insert_log(cls.table, cls.idname, cls, (set_query+where))
            pass
        if isinstance(row, bool) and row:
            row = where[cls.idname]
        return row

    public static function update(array $set, bool $log = true)
    {
        $where = array(static::$idname => $set['id']);
        unset($set['id']);
        $connection = database::instance();
        $row        = $connection->update(static::$table, static::$idname, $set, $where, self::$delete_cache);
        if ($log) {
            log::insert_log(static::$table, static::$idname, __FUNCTION__, array_merge($set, $where));
        }
        if (is_bool($row) && $row) {
            $row = $where[static::$idname];
        }

        return $row;
    }

    public static function delete(int $id)
    {
        $where      = array(static::$idname => $id);
        $connection = database::instance();
        $row        = $connection->delete(static::$table, static::$idname, $where, self::$delete_cache);
        log::insert_log(static::$table, static::$idname, __FUNCTION__, $where);
        return $row;
    }

    public static function copy(int $id)
    {
        $row = static::getById($id);
        if (isset($row['foto'])) {
            $foto_copy = $row['foto'];
            unset($row['foto']);
        }
        if (isset($row['archivo'])) {
            unset($row['archivo']);
        }
        $fields     = table::getByname(static::$table);
        $insert     = database::create_data($fields, $row);
        $connection = database::instance();
        $row        = $connection->insert(static::$table, static::$idname, $insert, self::$delete_cache);
        if (is_int($row) && $row > 0) {
            $last_id = $row;
            if (isset($foto_copy)) {
                $new_fotos = array();
                foreach ($foto_copy as $key => $foto) {
                    $copiar      = image::copy($foto, $last_id, $foto['folder'], $foto['subfolder'], $last_id, '');
                    $new_fotos[] = $copiar['file'][0];
                    image::regenerar($copiar['file'][0]);
                }
                $update = array('id' => $last_id, 'foto' => functions::encode_json($new_fotos));
                static::update($update);
            }
            log::insert_log(static::$table, static::$idname, __FUNCTION__, $insert);
            return $last_id;
        } else {
            return $row;
        }
    }

    public static function getByCookie(string $cookie, bool $estado_carro = true)
    {
        $where = array("cookie_pedido" => $cookie);
        if ($estado_carro) {
            $where['idpedidoestado'] = 1;
        }
        $connection = database::instance();
        $row        = $connection->get(static::$table, static::$idname, $where);
        return (count($row) == 1) ? $row[0] : $row;
    }
    public static function getByIdusuario(int $idusuario, bool $estado_carro = true)
    {
        $where = array("idusuario" => $idusuario);
        if ($estado_carro) {
            $where['idpedidoestado'] = 1;
        }
        $condition  = array('order' => static::$idname . ' DESC');
        $connection = database::instance();
        $row        = $connection->get(static::$table, static::$idname, $where, $condition);
        return ($estado_carro && count($row) > 0) ? $row[0] : $row;
    }
}
