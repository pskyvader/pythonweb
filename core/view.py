from pathlib import Path
from jinja2 import Template, Environment, select_autoescape


class view:
    extension = 'html'
    content_url = {}
    data = {}
    theme = ''
    resources=''
    html = """
        <html>
            %(content)s
        </html>
    """
    @staticmethod
    def add(key, value):
        view.data[key] = value

    @staticmethod
    def add_array(data):
        view.data = data

    @staticmethod
    def reset():
        view.data = {}

    @staticmethod
    def render(template, minify=True):
        theme = view.get_theme()
        template_url = theme + template + "." + view.extension
        my_file = Path(template_url)
        if not my_file.is_file():
            body = view.html % {  # Fill the above html template in
                'content': " <body>Error: El archivo " + template_url + " no existe </body>"
            }
            return body

        if template_url in view.content_url:
            content = view.content_url[template_url]
        else:
            with open(template_url, 'r') as f:
                content = view.content_url[template_url] = f.read()

        body = view.render_template(content)

        # if minify and not return_body and cache.is_cacheable():
        #    body = mini.html(body)

        view.reset()
        return body

    @staticmethod
    def render_template(content):
        env = Environment(autoescape=select_autoescape(
            enabled_extensions=('html', 'xml'), default_for_string=True, ),trim_blocks=True,lstrip_blocks=True)
        #template = Template(content)
        template=env.from_string(content)
        content = template.render(view.data)
        return content

    @staticmethod
    def css(return_css=False,combine=True,array_only=False):
        from core.app import app
        if app.post.getfirst("ajax") is None:
            return ''

        theme = view.get_theme()
        
        if (self::$resources == '') {
            $resources       = file_get_contents($theme . 'resources.json');
            self::$resources = json_decode($resources, true);
        }
        $css           = array();
        $locales       = array();
        $no_combinados = array();
        $nuevo         = 0;
        foreach (self::$resources['css'] as $key => $c) {
            $c['is_content'] = false;
            if ($c['local']) {
                $c['url'] = $theme . $c['url'];
                if (file_exists($c['url'])) {
                    if ($combine && $c['combine']) {
                        $fecha = functions::fecha_archivo($c['url'], true);
                        if ($fecha > $nuevo) {
                            $nuevo = $fecha;
                        }
                        $locales[] = $c;
                    } else {
                        if (filesize($c['url']) < 2000) {
                            $minifier = new mini_files\CSS($c['url']);
                            //$c['content_css'] = file_get_contents($c['url']);
                            $c['content_css'] = $minifier->minify();
                            $c['is_content']  = true;
                        } else {
                            $c['url'] = app::$_path . functions::fecha_archivo($c['url']);
                        }
                        $no_combinados[] = $c;
                    }
                } else {
                    if (error_reporting()) {
                        exit("Recurso no existe:" . $c['url']);
                    }
                }
            } else {
                $c['url'] = functions::ruta($c['url']);
                $css[]    = $c;
            }
        }

        if ($combine && count($locales) > 0) {
            $dir  = app::get_dir();
            $file = 'resources-' . $nuevo . '-' . count($locales) . '.css';
            if (file_exists($dir . '/' . $file)) {
                if (isset($_COOKIE['loaded_css']) && $_COOKIE['loaded_css']) {
                    $defer = false;
                } else {
                    functions::set_cookie('loaded_css', true, time() + (31536000));
                    $defer = true;
                }
                $locales = array(array('url' => app::$_path . $file, 'media' => 'all', 'defer' => $defer, 'is_content' => false));
            } else {
                cache::delete_cache();
                if (isset($_COOKIE['loaded_css'])) {
                    functions::set_cookie('loaded_css', false, time() + (31536000));
                }
                if (is_writable($dir)) {
                    $minifier = null;
                    foreach ($locales as $key => $l) {
                        if ($minifier == null) {
                            $minifier = new mini_files\CSS($l['url']);
                        } else {
                            $minifier->add($l['url']);
                        }
                    }
                    array_map('unlink', glob($dir . "/*.css"));
                    $minify  = $minifier->minify($dir . '/' . $file);
                    $locales = array(array('url' => app::$_path . $file, 'media' => 'all', 'defer' => true, 'is_content' => false));
                } else {
                    foreach ($locales as $key => $l) {
                        $locales[$key]['url'] = app::$_path . functions::fecha_archivo($l['url']);
                    }
                }
            }
        }
        $css = array_merge($no_combinados, $locales, $css);

        if ($array_only) {
            return array($css, $nuevo);
        } else {
            self::set('js', array());
            self::set('is_css', true);
            self::set('css', $css);

            if ($return) {
                $theme        = self::get_theme();
                $template_url = $theme . 'resources' . "." . self::EXTENSION_TEMPLATES;
                $content      = file_get_contents($template_url);
                return self::render_template(self::$data, $content);
            } else {
                self::render('resources');
            }
        }
    }

















    @staticmethod
    def js(return_js=False):
        return ''

    @staticmethod
    def set_theme(theme):
        view.theme = theme

    @staticmethod
    def get_theme():
        return view.theme
