from pathlib import Path
from .image import image


class file(image):
    types = ["application/zip", "application/x-zip-compressed", "application/octet-stream", "application/postscript", "application/msword", "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.openxmlformats-officedocument.spreadsheetml.template", "application/vnd.openxmlformats-officedocument.presentationml.template", "application/vnd.openxmlformats-officedocument.presentationml.slideshow",
             "application/vnd.openxmlformats-officedocument.presentationml.presentation", "application/vnd.openxmlformats-officedocument.presentationml.slide", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template", "application/vnd.ms-excel.addin.macroEnabled.12", "application/vnd.ms-excel.sheet.binary.macroEnabled.12", "application/pdf", "application/download"]
    extensions = ["zip", "doc", "docx", "dotx", "xls", "xlsx", "xltx",
                  "xlam", "xlsb", "ppt", "pptx", "potx", "ppsx", "sldx", "pdf"]


    public static function upload_tmp($modulo = '')
    {
        $respuesta = array('exito' => false, 'mensaje' => '');
        if (isset($_FILES)) {
            $archivos = array();

            if (isset($_FILES['file'])) {
                $file_ary = functions::reArrayFiles($_FILES['file']);
            } else {
                $file_ary = $_FILES;
            }

            foreach ($file_ary as $key => $files) {
                $archivo            = self::upload($files, 'tmp');
                $respuesta['exito'] = $archivo['exito'];
                if (!$archivo['exito']) {
                    $respuesta['mensaje'] = $archivo['mensaje'];
                    break;
                } else {
                    $name           = self::nombre_archivo($archivo['name'], '');
                    $archivo['url'] = self::get_upload_url() . $archivo['folder'] . '/' . $name;
                    $respuesta['mensaje'] .= $archivo['original_name'] . ' <br/>';
                    $archivos[] = $archivo;

                }
            }
            $respuesta['archivos'] = $archivos;
        } else {
            $respuesta['mensaje'] = 'No se encuentran archivos a subir';
        }

        return $respuesta;
    }

    @staticmethod
    def delete(cls, folder, file_name='', subfolder='', sub=''):
        import shutil
        if "" == file_name and '' != subfolder:
            url = cls.get_upload_dir() + folder + '/' + subfolder + '/'
            my_file = Path(url)
            if my_file.is_dir():
                shutil.rmtree(url)
        elif '' == file_name and '' == subfolder:
            url = cls.get_upload_dir() + folder + '/'
            my_file = Path(url)
            if my_file.is_dir():
                shutil.rmtree(url)
        else:
            if '' != subfolder:
                subfolder += '/'

            if '' != sub:
                sub += '/'

            url = cls.get_upload_dir() + folder + '/' + \
                subfolder + sub + file_name['url']
            my_file = Path(url)
            if my_file.is_file():
                my_file.unlink()
