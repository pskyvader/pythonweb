from core.cache import cache


class base:
    url        = []
    metadata   = {'title' : '', 'keywords' : '', 'description' : ''}
    breadcrumb = []
    modulo     = []
    seo        = []

    def init(self, var: list):
        from inspect import signature
        import inspect

        if len(var) == 0:
            var = ['index']

        if hasattr(self, var[0]) and callable(getattr(self, var[0])):
            fun = var[0]
            del var[0]
            method = getattr(self, fun)
            sig = signature(method)
            params = sig.parameters
            if 'self' in params:
                if 'var' in params:
                    ret = method(self, var=var)
                else:
                    ret = method(self)
            else:
                if 'var' in params:
                    ret = method(var=var)
                else:
                    ret = method()
        else:
            ret = {
                'error': 404
            }
        return ret



    @classmethod
    def __init__(cls,idseo, cache=True):
        if not cache:
            cache.set_cache(False)
        
        $this->seo               = seo_model.getById($idseo)
        $this->url               = array($this->seo['url'])
        $this->breadcrumb[]      = array('url' : functions.generar_url(array($this->seo['url'])), 'title' : $this->seo['titulo'])
        $this->metadata['image'] = image.generar_url(image.portada($this->seo['foto']), 'social')
        $this->metadata['modulo'] = (new \ReflectionClass($this))->getShortName()
        $moduloconfiguracion     = moduloconfiguracion_model.getByModulo($this->seo['modulo_back'])
        if (isset($moduloconfiguracion[0])) {
            $modulo = modulo_model.getAll(array('idmoduloconfiguracion' : $moduloconfiguracion[0], 'tipo' : $this->seo['tipo_modulo']), array('limit' : 1))
            if (isset($modulo[0])) {
                $this->modulo = $modulo[0]
            }
        }
    }
    public function meta($meta)
    {
        $this->metadata['title']            = (isset($meta['titulo']) && $meta['titulo'] != '') ? $meta['titulo'] : $this->metadata['title']
        $this->metadata['keywords_text']    = (isset($meta['keywords']) && $meta['keywords'] != '') ? $meta['keywords'] : $this->metadata['keywords_text']
        $this->metadata['description_text'] = (isset($meta['resumen']) && $meta['resumen'] != '') ? $meta['resumen'] : $this->metadata['description_text']
        $this->metadata['description_text'] = (isset($meta['descripcion']) && $meta['descripcion'] != '') ? $meta['descripcion'] : $this->metadata['description_text']
        $this->metadata['description_text'] = (isset($meta['metadescripcion']) && $meta['metadescripcion'] != '') ? $meta['metadescripcion'] : $this->metadata['description_text']
        if isset($meta['foto']) && $meta['foto']!='':
            $social=image.generar_url(image.portada($meta['foto']), 'social')
            if $social!='':
                $this->metadata['image'] = $social
            }
        }
    }

    protected function lista($row, $url = 'detail', $recorte = 'foto1')
    {
        $lista = array()
        foreach ($row as $key : $v) {
            $portada = image.portada($v['foto'])
            $c       = array(
                'title'       : $v['titulo'],
                'image'       : image.generar_url($portada, $recorte),
                'description' : $v['resumen'],
                'srcset'      : array(),
                'url'         : functions.url_seccion(array($this->url[0], $url), $v),
            )
            $src = image.generar_url($portada, $recorte, 'webp')
            if ($src != '') {
                $c['srcset'][] = array('media' : '', 'src' : $src, 'type' : 'image/webp')
            }
            $lista[] = $c
        }
        return $lista
    }