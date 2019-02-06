from pathlib import Path
from jinja2 import Template

class view:
    extension = 'html'
    content_url = {}
    data = {}
    theme = ''

    @staticmethod
    def add(key, value):
        view.data[key] = value


    @staticmethod
    def add_array(data):
        view.data=data

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
        template = Template(content)
        content= template.render(view.data)
        return content



    @staticmethod
    def css(return_css=False):
        return ''

    @staticmethod
    def set_theme(theme):
        view.theme = theme

    @staticmethod
    def get_theme():
        return view.theme
