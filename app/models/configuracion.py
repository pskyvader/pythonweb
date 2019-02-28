from .base_model import base_model


class configuracion(base_model):
    idname = 'idconfiguracion'
    table = 'configuracion'

    @classmethod
    def getByVariable(cls, variable:str):
        $where      = array('variable' => $variable);
        $condicion  = array('limit' => 1);
        $connection = database::instance();
        $row        = $connection->get(static::$table, static::$idname, $where, $condicion);
        return (count($row) == 1) ? $row[0]['valor'] : false;
    }

    public static function setByVariable(string $variable, string $valor)
    {
        $where      = array('variable' => $variable);
        $condicion  = array('limit' => 1);
        $connection = database::instance();
        $row        = $connection->get(static::$table, static::$idname, $where, $condicion);

        if (count($row) == 0) {
            $row = self::insert(array('variable' => $variable, 'valor' => $valor));
        } else {
            $row = self::update(array('variable' => $variable, 'valor' => $valor, 'id' => $row[0][0]));
        }
        return $row;
    }