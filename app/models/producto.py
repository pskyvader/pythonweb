from core.app import app
from core.database import database
from .base_model import base_model
import datetime
import json


class producto(base_model):
    idname = 'idproducto'
    table = 'producto'
    delete_cache = False


    @classmethod
    def getAll(cls, where={}, condiciones={}, select=""):
        limit = None
        idproductocategoria = None
        return_total = None
        connection = database.instance()
        # fields     = table.getByname(cls.table)
        fields = {}
        if 'estado' not in where and app.front and 'estado' in fields:
            where['estado'] = True

        if 'idproductocategoria' in where:
            if 'idproductocategoria' in fields:
                idproductocategoria = where['idproductocategoria']
                if 'limit' in condiciones:
                    limit = condiciones['limit']
                    limit2 = 0
                    del condiciones['limit']

                if 'limit2' in condiciones:
                    if limit == None:
                        limit = 0
                    limit2 = condiciones['limit2']
                    del condiciones['limit2']
            del where['idproductocategoria']

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
    
    public static function getAll(array $where = array(), array $condiciones = array(), string $select = "")
    {
        $connection = database::instance();
        if (!isset($where['estado']) && app::$_front) {
            $where['estado'] = true;
        }
        if (isset($where['idproductocategoria'])) {
            $idproductocategoria = $where['idproductocategoria'];
            unset($where['idproductocategoria']);
            if (isset($condiciones['limit'])) {
                $limit  = $condiciones['limit'];
                $limit2 = 0;
                unset($condiciones['limit']);
            }
            if (isset($condiciones['limit2'])) {
                if (!isset($limit)) {
                    $limit = 0;
                }

                $limit2 = $condiciones['limit2'];
                unset($condiciones['limit2']);
            }
        }

        if (!isset($condiciones['order'])) {
            $condiciones['order'] = 'orden ASC';
        }

        if (isset($condiciones['palabra'])) {
            $fields                = table::getByname(static::$table);
            $condiciones['buscar'] = array();
            if (isset($fields['titulo'])) {
                $condiciones['buscar']['titulo'] = $condiciones['palabra'];
            }

            if (isset($fields['keywords'])) {
                $condiciones['buscar']['keywords'] = $condiciones['palabra'];
            }

            if (isset($fields['descripcion'])) {
                $condiciones['buscar']['descripcion'] = $condiciones['palabra'];
            }

            if (isset($fields['metadescripcion'])) {
                $condiciones['buscar']['metadescripcion'] = $condiciones['palabra'];
            }

        }

        if ($select == 'total') {
            $return_total = true;
            if (isset($idproductocategoria)) {
                $select = '';
            }
        }
        $row = $connection->get(static::$table, static::$idname, $where, $condiciones, $select);
        foreach ($row as $key => $value) {
            if (isset($row[$key]['idproductocategoria'])) {
                $row[$key]['idproductocategoria'] = functions::decode_json($row[$key]['idproductocategoria']);
                if (isset($idproductocategoria) && !in_array($idproductocategoria, $row[$key]['idproductocategoria'])) {
                    unset($row[$key]);
                }
            }
            if (isset($row[$key]) && isset($row[$key]['foto'])) {
                $row[$key]['foto'] = functions::decode_json($row[$key]['foto']);
            }
            if (isset($row[$key]) && isset($row[$key]['archivo'])) {
                $row[$key]['archivo'] = functions::decode_json($row[$key]['archivo']);
            }
        }

        if (isset($idproductocategoria)) {
            $row = array_values($row);
        }

        if (isset($limit)) {
            if ($limit2 == 0) {
                $row = array_slice($row, $limit2, $limit);
            } else {
                $row = array_slice($row, $limit, $limit2);
            }
        }
        if (isset($return_total)) {
            return count($row);
        }

        $variables = array();
        if (isset($where['tipo'])) {
            $variables['tipo'] = $where['tipo'];
        }
        $cat        = productocategoria::getAll($variables);
        $categorias = array();
        foreach ($cat as $key => $c) {
            $categorias[$c[0]] = array('descuento' => $c['descuento'], 'descuento_fecha' => $c['descuento_fecha']);
        }

        foreach ($row as $key => $v) {
            if (isset($row[$key]['precio'])) {
                $row[$key]['precio_final'] = $row[$key]['precio'];
                $descuento                 = 0;
                if ($v['descuento'] != 0) {
                    $descuento = $v['descuento'];
                    $fechas    = $v['descuento_fecha'];
                } elseif (isset($categorias[$v['idproductocategoria'][0]]) && $categorias[$v['idproductocategoria'][0]]['descuento'] != 0) {
                    $descuento = $categorias[$v['idproductocategoria'][0]]['descuento'];
                    $fechas    = $categorias[$v['idproductocategoria'][0]]['descuento_fecha'];
                }

                if ($descuento > 0 && $descuento < 100) {
                    $fechas = explode(' - ', $fechas);
                    $fecha1 = strtotime(str_replace('/', '-', $fechas[0]));
                    $fecha2 = strtotime(str_replace('/', '-', $fechas[1]));
                    $now    = time();
                    if ($fecha1 < $now && $now < $fecha2) {
                        $precio_descuento = (($row[$key]['precio']) * $descuento) / 100;
                        $precio_final     = $row[$key]['precio'] - $precio_descuento;
                        if ($precio_final < 1) {
                            $precio_final = 1;
                        }

                        $row[$key]['precio_final'] = (int) $precio_final;
                    }
                }
            }
        }
        return $row;
    }

    public static function getById(int $id)
    {
        $where = array(static::$idname => $id);
        if (app::$_front) {
            $fields = table::getByname(static::$table);
            if (isset($fields['estado'])) {
                $where['estado'] = true;
            }

        }
        $connection = database::instance();
        $row        = $connection->get(static::$table, static::$idname, $where);
        if (count($row) == 1) {
            $row[0]['idproductocategoria'] = functions::decode_json($row[0]['idproductocategoria']);
            if (isset($idproductocategoria) && !in_array($idproductocategoria, $row[0]['idproductocategoria'])) {
                unset($row[0]);
            }
            if (isset($row[0]) && isset($row[0]['foto'])) {
                $row[0]['foto'] = functions::decode_json($row[0]['foto']);
            }
            if (isset($row[0]) && isset($row[0]['archivo'])) {
                $row[0]['archivo'] = functions::decode_json($row[0]['archivo']);
            }

            if (isset($row[0]) && isset($row[0]['precio'])) {

                $cat        = productocategoria::getById($row[0]['idproductocategoria'][0]);
                $categorias = array();
                if (count($cat) > 0) {
                    $categorias[$cat[0]] = array('descuento' => $cat['descuento'], 'descuento_fecha' => $cat['descuento_fecha']);
                }

                $row[0]['precio_final'] = $row[0]['precio'];
                $descuento              = 0;
                if ($row[0]['descuento'] != 0) {
                    $descuento = $row[0]['descuento'];
                    $fechas    = $row[0]['descuento_fecha'];
                } elseif (isset($categorias[$row[0]['idproductocategoria'][0]]) && $categorias[$row[0]['idproductocategoria'][0]]['descuento'] != 0) {
                    $descuento = $categorias[$row[0]['idproductocategoria'][0]]['descuento'];
                    $fechas    = $categorias[$row[0]['idproductocategoria'][0]]['descuento_fecha'];
                }

                if ($descuento > 0 && $descuento < 100) {
                    $fechas = explode(' - ', $fechas);
                    $fecha1 = strtotime(str_replace('/', '-', $fechas[0]));
                    $fecha2 = strtotime(str_replace('/', '-', $fechas[1]));
                    $now    = time();
                    if ($fecha1 < $now && $now < $fecha2) {
                        $precio_descuento = (($row[0]['precio']) * $descuento) / 100;
                        $precio_final     = $row[0]['precio'] - $precio_descuento;
                        if ($precio_final < 1) {
                            $precio_final = 1;
                        }

                        $row[0]['precio_final'] = (int) $precio_final;
                    }
                }
            }

        }
        return (count($row) == 1) ? $row[0] : $row;
    }

    public static function update(array $set, bool $log = true)
    {
        $where = array(static::$idname => $set['id']);
        unset($set['id']);
        $connection = database::instance();
        if (app::$_front) {
            $row = $connection->update(static::$table, static::$idname, $set, $where, self::$delete_cache);
        } else {
            $row = $connection->update(static::$table, static::$idname, $set, $where);
        }
        if ($log) {
            log::insert_log(static::$table, static::$idname, __FUNCTION__, array_merge($set, $where));
        }
        if (is_bool($row) && $row) {
            $row = $where[static::$idname];
        }

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
        $row['idproductocategoria'] = functions::encode_json($row['idproductocategoria']);
        $fields                     = table::getByname(static::$table);
        $insert                     = database::create_data($fields, $row);
        $connection                 = database::instance();
        $row                        = $connection->insert(static::$table, static::$idname, $insert);
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

}
