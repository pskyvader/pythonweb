from pathlib import Path
from jinja2 import Template, Environment, select_autoescape
from core.functions import functions
from os.path import getsize
import json

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
        if(view.resources==''):
            with open(theme+'resources.json') as f:
                view.resources = json.load(f)
        
        css           = [];
        locales       = [];
        no_combinados = [];
        nuevo         = 0;

        directory=app.url['base'] + 'static/' if app.front else  app.url['admin'] + 'static/'

        for c in view.resources['css']:
            c['is_content'] = False;
            if c['local']:
                url_tmp=c['url']
                c['url'] = theme + c['url']
                my_file = Path(c['url'])
                if not my_file.is_file():
                    if combine and c['combine']:
                        fecha = functions.fecha_archivo(c['url'],True)
                        if (fecha > nuevo):
                            nuevo = fecha;
                        locales.append(c)
                    else:
                        if getsize(c['url']) < 2000:
                            c['content_css'] = open(c['url'], "r").read()
                            c['is_content']  = True;
                        else:
                            c['url'] = directory + functions.fecha_archivo(c['url'],False,url_tmp)

                        no_combinados.append(c)
                else:
                    if app.config['debug']:
                        return "Recurso no existe:" + c['url']
            else:
                c['url'] = functions.ruta(c['url'])
                css.append(c)
            
        

        if combine and len(locales) > 0:
            file = 'resources-' + nuevo + '-' + len(locales) + '.css';
            my_file = Path(directory+'resources/'+file)
            if my_file.is_file():
                if functions.get_cookie('loaded_css')!=False:
                    defer = False
                else:
                    functions.set_cookie('loaded_css', True, time() + (31536000));
                    defer = True
                
                locales = array(array('url' => app::_path . file, 'media' => 'all', 'defer' => defer, 'is_content' => false));
            } else {
                cache::delete_cache();
                if (isset(_COOKIE['loaded_css'])) {
                    functions::set_cookie('loaded_css', false, time() + (31536000));
                }
                if (is_writable(dir)) {
                    minifier = null;
                    foreach (locales as key => l) {
                        if (minifier == null) {
                            minifier = new mini_files\CSS(l['url']);
                        } else {
                            minifier->add(l['url']);
                        }
                    }
                    array_map('unlink', glob(dir . "/*.css"));
                    minify  = minifier->minify(dir . '/' . file);
                    locales = array(array('url' => app::_path . file, 'media' => 'all', 'defer' => true, 'is_content' => false));
                } else {
                    foreach (locales as key => l) {
                        locales[key]['url'] = app::_path . functions::fecha_archivo(l['url']);
                    }
                }
            }
        }
        css = array_merge(no_combinados, locales, css);

        if (array_only) {
            return array(css, nuevo);
        } else {
            self::set('js', array());
            self::set('is_css', true);
            self::set('css', css);

            if (return) {
                theme        = self::get_theme();
                template_url = theme . 'resources' . "." . self::EXTENSION_TEMPLATES;
                content      = file_get_contents(template_url);
                return self::render_template(self::data, content);
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
