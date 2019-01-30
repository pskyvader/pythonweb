
class view:
    html = """
    <html>
        <body>
            %(body)s
        </body>
    </html>
    """
    data = {}

    @staticmethod
    def add(key, value):
        view.data[key] = value

    @staticmethod
    def render():
        data_return = []
        for key, value in view.data.items():
            a = '<div>'+key+':'+value+'</div>'
            data_return.append(a)
        body = '<br/>'.join(data_return)

        body = view.html % {  # Fill the above html template in
            'body': body
        }

        return body
