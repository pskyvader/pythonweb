from pathlib import Path
class view:
    extension='html'
    content_url={}
    html = """
    <html>
        %(content)s
    </html>
    """
    data = {}

    @staticmethod
    def add(key, value):
        view.data[key] = value

    @staticmethod
    def render(template,minify=False,return_body=False):
        theme='test'
        template_url = theme +template + "." + view.extension;
        my_file = Path(template_url)
        if not my_file.is_file():
            body = view.html % {  # Fill the above html template in
                'content': " <body>Error: El archivo " +template_url + " no existe </body>"
            }
            return body
        
        if template_url in view.content_url:
            content = view.content_url[template_url]
        else:
            with open(template_url, 'r') as f:
                content=view.content_url[template_url] = f.read()
        
        str_content = view.render_template(content)

        #if minify and not return_body and cache.is_cacheable():
        #    str_content = mini.html(str_content)

        view.reset()
        if return_body:
            return str_content
        else:
            body=str_content
            #cache.add_cache(str_content)
        
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
