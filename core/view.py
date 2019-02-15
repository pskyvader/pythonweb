from pathlib import Path
import os
import json


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
            content = view.content_url[template_url] = open(
                template_url, "r").read()

        body = view.render_template(content)

        # if minify and not return_body and cache.is_cacheable():
        #    body = mini.html(body)

        view.reset()
        return body

    @staticmethod
    def render_template(content):
        from jinja2 import Template
        #env = Environment(trim_blocks=True, lstrip_blocks=True)
        template = Template(content)
        #template = env.from_string(content)
        content = template.render(view.data)
        return content

    @staticmethod
    def css(combine=True, array_only=False):
        from core.functions import functions
        from core.app import app
        if app.post.getfirst("ajax") is not None:
            return ''

        theme = view.get_theme()
        if(len(view.resources) == 0):
            with open(theme+'resources.json') as f:
                view.resources = json.load(f)

        css = []
        locales = []
        no_combinados = []
        nuevo = 0

        base_url = app.url['base'] + \
            'static/' if app.front else app.url['admin'] + 'static/'

        for c in view.resources['css']:
            c['is_content'] = False
            if c['local']:
                c['url_tmp'] = c['url']
                c['url'] = theme + c['url']
                my_file = Path(c['url'])
                if my_file.is_file():
                    if combine and c['combine']:
                        fecha = functions.fecha_archivo(c['url'], True)
                        if (fecha > nuevo):
                            nuevo = fecha
                        locales.append(c)
                    else:
                        if os.path.getsize(c['url']) < 2000:
                            c['content_css'] = open(c['url'], "r").read()
                            c['is_content'] = True
                        else:
                            c['url'] = base_url + \
                                functions.fecha_archivo(
                                    c['url'], False, c['url_tmp'])
                        no_combinados.append(c)
                else:
                    if app.config['debug']:
                        return "Recurso no existe:" + c['url']
            else:
                c['url'] = functions.ruta(c['url'])
                css.append(c)

        if combine and len(locales) > 0:
            dir_resources = theme+'resources/'
            file = 'resources-' + str(nuevo) + '-' + str(len(locales)) + '.css'
            my_file = Path(dir_resources+file)
            if my_file.is_file():
                if functions.get_cookie('loaded_css') != False:
                    defer = False
                else:
                    functions.set_cookie('loaded_css', True, (31536000))
                    defer = True

                locales = [{'url': base_url+'resources/' + file,
                            'media': 'all', 'defer': defer, 'is_content': False}]
            else:
                # cache.delete_cache()
                if functions.get_cookie('loaded_css') != False:
                    functions.set_cookie('loaded_css', True, (31536000))

                if os.access(dir_resources, os.R_OK):
                    combine_files = ''
                    for l in locales:
                        combine_files += '\n' + open(l['url'],
                                                     "r", encoding='utf-8').read()

                    test = os.listdir(dir_resources)
                    for item in test:
                        if item.endswith(".css"):
                            os.remove(os.path.join(dir_resources, item))
                    file_write = open(dir_resources+file,
                                      'w', encoding='utf-8')
                    file_write.write(combine_files)
                    file_write.close()
                    locales = [{'url': base_url+'resources/' + file,
                                'media': 'all', 'defer': True, 'is_content': False}]
                else:
                    for l in locales:
                        l['url'] = base_url + \
                            functions.fecha_archivo(
                                l['url'], False, l['url_tmp'])

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
        if app.post.getfirst("ajax") is not None:
            return ''

        theme = view.get_theme()
        if(len(view.resources) == 0):
            with open(theme+'resources.json') as f:
                view.resources = json.load(f)
        js = []
        locales = []
        no_combinados = []
        nuevo = 0

        base_url = app.url['base'] + \
            'static/' if app.front else app.url['admin'] + 'static/'

        for c in view.resources['js']:
            c['is_content'] = False
            if c['local']:
                c['url_tmp'] = c['url']
                c['url'] = theme + c['url']
                my_file = Path(c['url'])
                if my_file.is_file():
                    if combine and c['combine'] and not c['defer']:
                        fecha = functions.fecha_archivo(c['url'], True)
                        if (fecha > nuevo):
                            nuevo = fecha
                        locales.append(c)
                    else:
                        c['url'] = base_url + \
                            functions.fecha_archivo(
                                c['url'], False, c['url_tmp'])
                        c['defer'] = 'async defer' if c['defer'] else ''
                        no_combinados.append(c)
                else:
                    if app.config['debug']:
                        return "Recurso no existe:" + c['url']
            else:
                c['url'] = functions.ruta(c['url'])
                c['defer'] = 'async defer' if c['defer'] else ''
                js.append(c)

        if combine and len(locales) > 0:
            dir_resources = theme+'resources/'
            file = 'resources-' + str(nuevo) + '-' + str(len(locales)) + '.js'
            my_file = Path(dir_resources+file)
            if my_file.is_file():
                if functions.get_cookie('loaded_js') != False:
                    defer = ''
                else:
                    functions.set_cookie('loaded_js', True, (31536000))
                    defer = 'async defer'

                locales = [{'url': base_url+'resources/' + file,
                            'media': 'all', 'defer': defer, 'is_content': False}]
            else:
                # cache.delete_cache()
                if functions.get_cookie('loaded_js') != False:
                    functions.set_cookie('loaded_js', True, (31536000))

                if os.access(dir_resources, os.R_OK):
                    combine_files = ''
                    for l in locales:
                        combine_files += '\n' + open(l['url'],
                                                     "r", encoding='utf-8').read()

                    test = os.listdir(dir_resources)
                    for item in test:
                        if item.endswith(".js"):
                            os.remove(os.path.join(dir_resources, item))
                    file_write = open(dir_resources+file,
                                      'w', encoding='utf-8')
                    file_write.write(combine_files)
                    file_write.close()
                    locales = [{'url': base_url+'resources/' + file,
                                'media': 'all', 'defer': 'async defer', 'is_content': False}]
                else:
                    for l in locales:
                        l['url'] = base_url + \
                            functions.fecha_archivo(
                                l['url'], False, l['url_tmp'])

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
    def recorrer(type_resource='css',combine=False):
        from core.functions import functions
        from core.app import app
        theme = view.get_theme()
        if(len(view.resources) == 0):
            with open(theme+'resources.json') as f:
                view.resources = json.load(f)
        resource = []
        locales = []
        no_combinados = []
        nuevo = 0

        base_url = app.url['base'] + \
            'static/' if app.front else app.url['admin'] + 'static/'


        for c in view.resources[type_resource]:
            c['is_content'] = False
            if c['local']:
                c['url_tmp'] = c['url']
                c['url'] = theme + c['url']
                my_file = Path(c['url'])
                if my_file.is_file():


                    if combine and c['combine'] and ((type_resource=='js' and not c['defer']) or type_resource=='css'):
                        fecha = functions.fecha_archivo(c['url'], True)
                        if (fecha > nuevo):
                            nuevo = fecha
                        locales.append(c)
                    else:
                        if type_resource=='css' and os.path.getsize(c['url']) < 2000:
                            c['content_css'] = open(c['url'], "r").read()
                            c['is_content'] = True
                        else:
                            c['url'] = base_url + functions.fecha_archivo( c['url'], False, c['url_tmp'])
                            if type_resource=='js':
                                c['defer'] = 'async defer' if c['defer'] else ''
                        no_combinados.append(c)



                    if combine and c['combine']:
                        fecha = functions.fecha_archivo(c['url'], True)
                        if (fecha > nuevo):
                            nuevo = fecha
                        locales.append(c)
                    else:
                        if os.path.getsize(c['url']) < 2000:
                            c['content_css'] = open(c['url'], "r").read()
                            c['is_content'] = True
                        else:
                            c['url'] = base_url + functions.fecha_archivo( c['url'], False, c['url_tmp'])
                        no_combinados.append(c)


                else:
                    if app.config['debug']:
                        return "Recurso no existe:" + c['url']
            else:
                c['url'] = functions.ruta(c['url'])
                resource.append(c)

        for c in view.resources[type_resource]:
            c['is_content'] = False
            if c['local']:
                c['url_tmp'] = c['url']
                c['url'] = theme + c['url']
                my_file = Path(c['url'])
                if my_file.is_file():
                    if combine and c['combine'] and not c['defer']:
                        fecha = functions.fecha_archivo(c['url'], True)
                        if (fecha > nuevo):
                            nuevo = fecha
                        locales.append(c)
                    else:
                        c['url'] = base_url + \
                            functions.fecha_archivo(
                                c['url'], False, c['url_tmp'])
                        c['defer'] = 'async defer' if c['defer'] else ''
                        no_combinados.append(c)
                else:
                    if app.config['debug']:
                        return "Recurso no existe:" + c['url']
            else:
                c['url'] = functions.ruta(c['url'])
                c['defer'] = 'async defer' if c['defer'] else ''
                resource.append(c)
        return resource,locales,no_combinados,nuevo