<?php
namespace app\controllers\back\themes\{theme};

defined("APPPATH") or die("Acceso denegado");
use \app\models\{name} as {name}_model;
//use \app\models\administrador as administrador_model;
//use \app\models\moduloconfiguracion as moduloconfiguracion_model;
//use \app\models\modulo as modulo_model;
//use \app\models\table;
//use \core\functions;
//use \core\image;

class {name} extends base
{
    protected $url = array('{name}');
    protected $metadata = array('title' => '{name}','modulo'=>'{name}');
    protected $breadcrumb = array();
    public function __construct()
    {
        parent::__construct(new {name}_model);
    }
}

from .base import base
from app.models.{{class}} import {{class}} as {{class}}_model

#from core.app import app
#from core.functions import functions
#from .detalle import detalle as detalle_class
#from .lista import lista as lista_class


class {{class}}(base):
    url = ['{{class}}']
    metadata = {'title' : '{{class}}','modulo':'{{class}}'}
    breadcrumb = []
    def __init__(self):
        super().__init__({{class}}_model)