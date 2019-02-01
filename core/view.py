from pathlib import Path
class view:
    extension='html'
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
    def render(template,minify=False,return_body=False):
        theme='test'
        template_url = theme +template + "." + view.extension;
        my_file = Path(self.root+controller+'.py')
        if my_file.is_file():
        data_return = []
        for key, value in view.data.items():
            a = '<div>'+key+':'+value+'</div>'
            data_return.append(a)
        body = '<br/>'.join(data_return)

        body = view.html % {  # Fill the above html template in
            'body': body
        }

        return body

public static function render($template, $minify = true, $return = false)
    {
        $theme        = self::get_theme();
        $template_url = $theme . $template . "." . self::EXTENSION_TEMPLATES;
        if (!file_exists($template_url)) {
            throw new \Exception("Error: El archivo " . $template_url . " no existe", 1);
        }

        if (isset(self::$content_url[$template_url])) {
            $content = self::$content_url[$template_url];
        } else {
            $content                          = file_get_contents($template_url);
            self::$content_url[$template_url] = $content;
        }
        $str = self::render_template(self::$data, $content);
        if ($minify && !$return && cache::is_cacheable()) {
            $str = mini::html($str,array('collapse_whitespace'=>true));
        }

        self::reset();
        if ($return) {
            return $str;
        } else {
            /*ob_start();
            echo $str;
            $str = ob_get_contents();
            ob_end_clean();*/
            echo $str;
            cache::add_cache($str);
        }
    }