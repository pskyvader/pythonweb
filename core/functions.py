class functions():
    environ = {}

    @staticmethod
    def set_environ(environ):
        functions.environ = environ

    @staticmethod
    def generar_url(url, extra = {}, front_auto = True, front = True):
    {
        $url = implode('/', $url);
        if (is_array($extra) && count($extra) > 0) {
            $url .= "?" . http_build_query($extra);
        } elseif (count($_GET) > 0) {
            if (!is_bool($extra) || $extra) {
                $url .= "?" . http_build_query($_GET);
            }
        }
        $url = str_replace("%2F", "/", $url);
        $url = (($front_auto) ? (app::get_url()) : (app::get_url($front))) . $url;

        return $url;
    }

    @staticmethod
    def current_url():
        environ = functions.environ
        url = environ['wsgi.url_scheme']+'://'
        if environ.get('HTTP_HOST'):
            url += environ['HTTP_HOST']
        else:
            url += environ['SERVER_NAME']

            if environ['wsgi.url_scheme'] == 'https':
                if environ['SERVER_PORT'] != '443':
                    url += ':' + environ['SERVER_PORT']
            else:
                if environ['SERVER_PORT'] != '80':
                    url += ':' + environ['SERVER_PORT']
        url += environ['SCRIPT_NAME']
        url += environ['PATH_INFO']
        if environ['QUERY_STRING']:
            url += '?' + environ['QUERY_STRING']
        return url
