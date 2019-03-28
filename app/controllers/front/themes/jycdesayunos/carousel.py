from core.image import image
class carousel:
    sizes = [
        {'foto': 'foto1', 'size': '1200'},
        {'foto': 'foto2', 'size': '991'},
        {'foto': 'foto3', 'size': '768'},
        {'foto': 'foto4', 'size': '0'},
    ]


    def normal(self, row_carousel=[],titulo):
        ret = {'body': []}
        if len(row_carousel) > 0:
            thumb = []
            
            for key, c in row_carousel:
                foto = image.generar_url(c, 'thumb_carousel')

                portada = image.portada(b["foto"])
                foto = image.generar_url(portada, 'foto1')
                if foto != '':
                    thumb.append({'id': key, 'active': (key == 0)})

                    srcset = self.srcset(portada)

                    banner.append({
                        'srcset': srcset,
                        'title': b['titulo'],
                        'active': (key == 0),
                        'data': 'data-' if (key != 0) else '',
                        'foto': foto,
                        'texto1': b['texto1'],
                        'texto2': b['texto2'],
                        'link': functions.ruta(b['link']),
                        'background': image.generar_url(portada, 'color'),
                    })

            data = {}
            data['thumb'] = thumb
            data['banner'] = banner
            ret['body'].append(('banner', data))
        return ret



            foreach ($row_carousel as $key => $c) {
                if (isset($c)) {
                    $foto = image::generar_url($c, 'thumb_carousel');
                } else {
                    $foto = '';
                }
                if ('' != $foto) {
                    $foto_w = image::generar_url($c, 'thumb_carousel', 'webp');
                    if ('' != $foto_w) {
                        $srcset = array(array('url' => $foto_w, 'type' => 'image/webp'));
                    }
                    $thumb[] = array(
                        'srcset' => $srcset,
                        'id'     => $key,
                        'title'  => $titulo,
                        'active' => (0 == $key) ? 'active' : '',
                        'foto'   => $foto,
                    );
                }
            }

            $carousel = array();
            foreach ($row_carousel as $key => $c) {
                if (isset($c)) {
                    $foto = image::generar_url($c, 'foto1');
                } else {
                    $foto = '';
                }
                if ('' != $foto) {

                    $srcset = $this->srcset($c);

                    $carousel[] = array(
                        'id'       => $key,
                        'srcset'   => $srcset,
                        'title'    => $titulo,
                        'active'   => (0 == $key) ? 'active' : '',
                        'data'     => (0 != $key) ? 'data-' : '',
                        'foto'     => $foto,
                        'original' => image::generar_url($c, ''),
                    );
                }
            }
            view::set('thumb', $thumb);
            view::set('carousel', $carousel);
            view::render('carousel');
        }
    }

    public function srcset($foto_base)
    {
        $images = self::$sizes;
        $srcset = array();
        foreach ($images as $k => $size) {
            $foto = image::generar_url($foto_base, $size['foto'], 'webp');
            if ('' != $foto) {
                $srcset[] = array('media' => '(min-width: ' . $size['size'] . 'px)', 'url' => $foto, 'type' => 'image/webp');
            }
        }
        foreach ($images as $k => $size) {
            $foto = image::generar_url($foto_base, $size['foto']);
            if ('' != $foto) {
                $srcset[] = array('media' => '(min-width: ' . $size['size'] . 'px)', 'url' => $foto, 'type' => 'image/jpg');
            }
        }
        return $srcset;
    }
}
