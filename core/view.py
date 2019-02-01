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
            if not res[1]  # no es bloque if
            content = str_replace('{' + key + '}', d, content)

        data_return = []
        for key, value in view.data.items():
            a = '<div>'+key+':'+value+'</div>'
            data_return.append(a)
        body = '<br/>'.join(data_return)

        str_content = view.html % {  # Fill the above html template in
            'content': body
        }
        return str_content


public static function render_template(array $data, string $content)
 {$data2 = array()
   foreach ($data as $key=> $d) {
            if (is_array($d)) {// arrray de elementos foreach en vista
                               $array_open = "{foreach " . $key . "}"
                               $array_close = "{/foreach " . $key . "}"

                               $pos_open = strpos($content, $array_open)
                                $pos_close = strpos($content, $array_close)

                if ($pos_open != = false & & $pos_close != = false) { // existe el codigo foreach en vista?
                                                                      $subcontent1 = substr($content, $pos_open, ($pos_close - $pos_open));
                                                                      $subcontent = str_replace($array_open, "", $subcontent1);
                                                                      $sub = "";
                    foreach ($d as $k = > $s) { // rellenar recursivamente los elementos dentro del foreach
                                                $sub . = self:: render_template($s, $subcontent);                                                }
                    $content = str_replace($subcontent1, $sub, $content);
                    $content = str_replace($array_close, "", $content);} elseif(error_reporting()) {
                    throw new \Exception("Array no encontrado {$array_open}, o Tag mal cerrado", 1);}

            } else {// si no es array, se procesa despues para evitar conflictos de nombres repetidos dentro y fuera del bloque foreach en template
                    $data2[$key] = $d;}
      }
      foreach ($data2 as $key = > $d) {$res     = self:: template_if($content, $key, $d);
                                        $content = $res[0];
            if (!$res[1]) {// no es bloque if
                           $content = str_replace('{' . $key . '}', $d, $content);}
      }
      return $content;}

  @staticmethod
   def set_theme(theme):
        view.theme = theme

    @staticmethod
    def get_theme():
        return view.theme
