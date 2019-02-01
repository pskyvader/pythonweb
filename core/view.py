from pathlib import Path
from string import Template


class view:
    extension = 'html'
    content_url = {}
    data = {}
    theme = ''
    html = """
    <html>
        %(content)s
    </html>
    """

    @staticmethod
    def add(key, value):
        view.data[key] = value

    @staticmethod
    def reset():
        view.data = {}

    @staticmethod
    def render(template, minify=True, return_body=False):
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
        if return_body:
            return body
        else:
            return view.html % {  # Fill the above html template in
                'content': body
            }

    @staticmethod
    def render_template(content):
        data2 = {}
        for key, d in view.data.items():
            if isinstance(d, dict):  # es dictionary de elementos en vista
                array_open = "{foreach " + key + "}"
                array_close = "{/foreach " + key + "}"
                return False
            else:
                data2[key] = d

        for key, d in data2.items():
            res = view.template_if(content, key, d)
            content = res[0]
            if not res[1]:  # no es bloque if
                s = Template(content)
                dic = dict(key=d)
                content = s.substitute(dic)
        return content


    @staticmethod
    def set_theme(theme):
        view.theme = theme

    @staticmethod
    def get_theme():
        return view.theme
