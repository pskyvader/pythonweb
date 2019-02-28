from core.app import app
from core.database import database
from .base_model import base_model
from .productocategoria import productocategoria
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
            if idproductocategoria != None:
                select = ''

        row = connection.get(cls.table, cls.idname, where, condiciones, select)
        deleted = False
        for r in row:
            deleted = False
            if 'idproductocategoria' in r:
                r['idproductocategoria'] = json.loads(r['idproductocategoria'])
                if idproductocategoria != None and idproductocategoria not in r['idproductocategoria']:
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
            variables = {}
            if 'tipo' in where:
                variables['tipo'] = where['tipo']
            cat        = productocategoria.getAll(variables)
            categorias = {}
            for c in cat:
                categorias[c[0]] = {'descuento' : c['descuento'], 'descuento_fecha' : c['descuento_fecha']}

            for v in row:
                if 'precio' in v:
                    v['precio_final'] = v['precio']
                    descuento                 = 0
                    if v['descuento'] != 0:
                        descuento = v['descuento']
                        fechas    = v['descuento_fecha']
                    elif v['idproductocategoria'][0] in categorias and categorias[v['idproductocategoria'][0]]['descuento'] != 0:
                        descuento = categorias[v['idproductocategoria'][0]]['descuento']
                        fechas    = categorias[v['idproductocategoria'][0]]['descuento_fecha']
                    if descuento > 0 and descuento < 100:
                        fechas = fechas.split(' - ')
                        fecha1 = datetime.datetime.strptime(fechas[0],'%d/%m/%Y %H:%M')
                        fecha2 = datetime.datetime.strptime(fechas[1],'%d/%m/%Y %H:%M')
                        now    = datetime.datetime.now()
                        if fecha1 < now and now < fecha2:
                            precio_descuento = ((v['precio']) * descuento) / 100
                            precio_final     = v['precio'] - precio_descuento
                            if precio_final < 1:
                                precio_final = 1
                            v['precio_final'] = int(precio_final)
            return row
    
    @classmethod
    def getById(cls, id: int):
        where = {cls.idname: id}
        if app.front:
            # fields     = table.getByname(cls.table)
            fields = {}
            if 'estado' in fields:
                where['estado'] = True

        connection = database.instance()
        row = connection.get(cls.table, cls.idname, where)
        if len(row) == 1:
            row[0]['idproductocategoria'] = json.loads(row[0]['idproductocategoria'])
            if 'foto' in row[0]:
                row[0]['foto'] = json.loads(row[0]['foto'])
            if 'archivo' in row[0]:
                row[0]['archivo'] = json.loads(row[0]['archivo'])


            if 'precio' in row[0]:
                cat        = productocategoria.getById(row[0]['idproductocategoria'][0])
                categorias = {}
                if len(cat) > 0:
                    categorias[cat[0]] = {'descuento' : cat['descuento'], 'descuento_fecha' : cat['descuento_fecha']}
                
                row[0]['precio_final'] = row[0]['precio']
                descuento              = 0
                if row[0]['descuento'] != 0:
                    descuento = row[0]['descuento']
                    fechas    = row[0]['descuento_fecha']
                elif row[0]['idproductocategoria'][0] in categorias and categorias[row[0]['idproductocategoria'][0]]['descuento'] != 0:
                    descuento = categorias[row[0]['idproductocategoria'][0]]['descuento']
                    fechas    = categorias[row[0]['idproductocategoria'][0]]['descuento_fecha']
                

                if (descuento > 0 && descuento < 100) {
                    fechas = explode(' - ', fechas)
                    fecha1 = strtotime(str_replace('/', '-', fechas[0]))
                    fecha2 = strtotime(str_replace('/', '-', fechas[1]))
                    now    = time()
                    if (fecha1 < now && now < fecha2) {
                        precio_descuento = ((row[0]['precio']) * descuento) / 100
                        precio_final     = row[0]['precio'] - precio_descuento
                        if (precio_final < 1) {
                            precio_final = 1
                        }

                        row[0]['precio_final'] = (int) precio_final
                    }
                }
            }

        return row[0] if len(row) == 1 else row

    public static function getById(int $id)
    {
        $where = array(static.$idname => $id)
        if (app.$_front) {
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
