from pathlib import Path
import os
import json
import codecs


class view:
    extension = 'html'
    content_url = {}
    data = {}
    theme = ''
    resources = {}
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
        '''Renderiza la vista segun view.data y la retorna'''
        theme = view.get_theme()
        template_url = theme + template + "." + view.extension
        my_file = Path(template_url)
        if not my_file.is_file():
            body = view.html % {  # Fill the above html template in
                'content': " <body>Error: El archivo " + template_url + " no existe </body>"
            }
            return body

        # if template_url in view.content_url:
        #    content = view.content_url[template_url]
        # else:
        #    content = view.content_url[template_url] =  codecs.open(template_url, encoding='utf-8').read()

        #body = view.render_template(content)
        body = view.render_template_url2(
            template + "." + view.extension, view.data)

        if minify:  # and not return_body and cache.is_cacheable():
            body = view.compress(body, 'html')

        view.reset()
        return body

    @staticmethod
    def render_multiple(template_list, minify=True):
        '''Renderiza la vista segun view.data y la retorna'''
        from jinja2 import Environment, FileSystemLoader
        theme = view.get_theme()
        env = Environment(
            loader=FileSystemLoader(theme)
        )

        for template, data in template_list:
            template_url = theme + template + "." + view.extension
            my_file = Path(template_url)
            if not my_file.is_file():
                body = view.html % {  # Fill the above html template in
                    'content': " <body>Error: El archivo " + template_url + " no existe </body>"
                }
                return body

        body = ''
        for template, data in template_list:
            #template = env.get_template(template + "." + view.extension)
            #body += template.render(data)
            body += view.render_unit(env, template, data)

        if minify:  # and not return_body and cache.is_cacheable():
            body = view.compress(body, 'html')

        return body

    @staticmethod
    def render_unit(env, template, data):
        if isinstance(data, dict):
            for k,d in data.items():
                if isinstance(d, dict) or isinstance(d, list) or isinstance(d, tuple):
                    d = view.render_unit(env, template, d)
        elif isinstance(data, list):
            for d in data:
                if isinstance(d, dict) or isinstance(d, list) or isinstance(d, tuple):
                    print(d)
                    d = view.render_unit(env, template, d)
        elif isinstance(data, tuple):
            data = view.render_unit(env, data(0), data(1))

        template = env.get_template(template + "." + view.extension)
        return template.render(data)

    @staticmethod
    def render_template2(content):
        from jinja2 import Template
        template = Template(content)
        content = template.render(view.data)
        return content

    @staticmethod
    def render_template_url2(template_url, data):
        from jinja2 import Environment, FileSystemLoader
        env = Environment(
            loader=FileSystemLoader(view.get_theme())
        )
        template = env.get_template(template_url)
        content = template.render(data)
        return content

    @staticmethod
    def render_template(content):
        from ibis import Template
        template = Template(content)
        content = template.render(view.data)
        return content

    @staticmethod
    def render_template_url(template_url):
        import ibis
        loader = ibis.loaders.FileLoader(view.get_theme())
        template = loader(template_url)
        content = template.render(view.data)
        return content

    @staticmethod
    def css(combine=True, array_only=False):
        from core.functions import functions
        from core.app import app
        if 'ajax' in app.post:
            return ''

        theme = view.get_theme()
        base_url = app.url['base'] + \
            'static/' if app.front else app.url['admin'] + 'static/'
        css, locales, no_combinados, nuevo, error = view.recorrer(
            'css', combine, theme, base_url)

        if error != '':
            return error

        if combine and len(locales) > 0:
            locales = view.combine_resources(
                'css', locales, theme, base_url, nuevo)

        css = no_combinados + locales + css

        if array_only:
            return [css, nuevo]
        else:
            view.add('js', [])
            view.add('is_css', True)
            view.add('css', css)
            return view.render('resources')

    @staticmethod
    def js(combine=True, array_only=False):
        from core.functions import functions
        from core.app import app
        if 'ajax' in app.post:
            return ''

        theme = view.get_theme()
        base_url = app.url['base'] + \
            'static/' if app.front else app.url['admin'] + 'static/'
        js, locales, no_combinados, nuevo, error = view.recorrer(
            'js', combine, theme, base_url)

        if error != '':
            return error

        if combine and len(locales) > 0:
            locales = view.combine_resources(
                'js', locales, theme, base_url, nuevo)

        js = no_combinados + locales + js

        if array_only:
            return [js, nuevo]
        else:
            view.add('css', [])
            view.add('is_css', False)
            view.add('js', js)
            return view.render('resources')

    @staticmethod
    def set_theme(theme):
        view.theme = theme

    @staticmethod
    def get_theme():
        return view.theme

    @staticmethod
    def recorrer(type_resource='css', combine=False, theme='', base_url=''):
        from core.functions import functions
        from core.app import app
        if(len(view.resources) == 0):
            with open(theme+'resources.json') as f:
                view.resources = json.load(f)
        resource = []
        locales = []
        no_combinados = []
        nuevo = 0
        error = ""
        for res in view.resources[type_resource]:
            c = res.copy()
            c['is_content'] = False
            if c['local']:
                c['url_tmp'] = c['url']
                c['url'] = theme + c['url']
                my_file = Path(c['url'])
                if my_file.is_file():
                    if combine and c['combine'] and ((type_resource == 'js' and not c['defer']) or type_resource == 'css'):
                        fecha = functions.fecha_archivo(c['url'], True)
                        if (fecha > nuevo):
                            nuevo = fecha
                        locales.append(c)
                    else:
                        if type_resource == 'css' and os.path.getsize(c['url']) < 8000:
                            c['content_css'] = open(c['url'], "r").read()
                            c['is_content'] = True
                        else:
                            c['url'] = base_url + \
                                functions.fecha_archivo(
                                    c['url'], False, c['url_tmp'])
                        no_combinados.append(c)
                else:
                    if app.config['debug']:
                        error = "Recurso no existe:" + c['url']
            else:
                c['url'] = functions.ruta(c['url'])
                resource.append(c)
        return resource, locales, no_combinados, nuevo, error

    @staticmethod
    def combine_resources(type_resource='css', locales={}, theme='', base_url='', nuevo=0):
        from core.functions import functions
        dir_resources = theme+'resources/'
        file = 'resources-' + str(nuevo) + '-' + \
            str(len(locales)) + '.'+type_resource
        my_file = Path(dir_resources+file)
        if my_file.is_file():
            if functions.get_cookie('loaded_'+type_resource) != False:
                defer = False
            else:
                functions.set_cookie('loaded_'+type_resource, True, (31536000))
                defer = True

            locales = [{'url': base_url+'resources/' + file,
                        'media': 'all', 'defer': defer, 'is_content': False}]
        else:
            # cache.delete_cache()
            if functions.get_cookie('loaded_'+type_resource) != False:
                functions.set_cookie('loaded_'+type_resource, True, (31536000))

            if os.access(dir_resources, os.R_OK):
                combine_files = ''
                for l in locales:
                    tmp = open(l['url'], "r", encoding='utf-8').read()
                    combine_files += '\n' + tmp

                test = os.listdir(dir_resources)
                for item in test:
                    if item.endswith("."+type_resource):
                        os.remove(os.path.join(dir_resources, item))
                file_write = open(dir_resources+file, 'w', encoding='utf-8')
                combine_files = view.compress(combine_files, type_resource)
                file_write.write(combine_files)
                file_write.close()
                locales = [{'url': base_url+'resources/' + file,
                            'media': 'all', 'defer': True, 'is_content': False}]
            else:
                for l in locales:
                    l['url'] = base_url + \
                        functions.fecha_archivo(l['url'], False, l['url_tmp'])
        return locales

    @staticmethod
    def compress(combine_files, type_resource):
        if type_resource == 'css':
            from csscompressor import compress
            combine_files = compress(combine_files)
        elif type_resource == 'js':
            from jsmin import jsmin
            combine_files = jsmin(combine_files)
        elif type_resource == 'html':
            from htmlmin import minify
            combine_files = minify(combine_files, True, True, True)
        return combine_files
