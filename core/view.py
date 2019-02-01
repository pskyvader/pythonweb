from pathlib import Path
from core import app


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
    def render_template(template_url):
        data_return = []
        for key, value in view.data.items():
            a = '<div>'+key+':'+value+'</div>'
            data_return.append(a)
        body = '<br/>'.join(data_return)

        str_content = view.html % {  # Fill the above html template in
            'content': body
        }
        return str_content

    @staticmethod
    def get_theme():
        if view.theme == '':
            view.theme = app.app.root + app.app.view_dir
        return view.theme
