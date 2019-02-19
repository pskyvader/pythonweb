from pathlib import Path

class image:
    types = ["image/webp", "image/bmp", "image/gif", "image/pjpeg", "image/jpeg", "image/svg+xml", "image/png", "video/webm", "video/mp4", "application/zip", "application/x-zip-compressed", "application/octet-stream", "application/postscript", "application/msword", "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.openxmlformats-officedocument.spreadsheetml.template", "application/vnd.openxmlformats-officedocument.presentationml.template",
             "application/vnd.openxmlformats-officedocument.presentationml.slideshow", "application/vnd.openxmlformats-officedocument.presentationml.presentation", "application/vnd.openxmlformats-officedocument.presentationml.slide", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template", "application/vnd.ms-excel.addin.macroEnabled.12", "application/vnd.ms-excel.sheet.binary.macroEnabled.12", "application/pdf", "application/download"]
    extensions = ["webp", "bmp", "ico", "gif", "jpeg", "jpg", "svg", "xml", "png", "webm", "mp4", "zip", "doc",
                  "docx", "dotx", "xls", "xlsx", "xltx", "xlam", "xlsb", "ppt", "pptx", "potx", "ppsx", "sldx", "pdf"]
    upload_dir = ''
    upload_url = ''
    @staticmethod
    def delete(folder, file = '', subfolder = '', sub = ''):
        if "" == file and '' != subfolder:
            url = image.get_upload_dir() + folder + '/' +subfolder +'/'
            my_file = Path(url)
            if my_file.is_file():
                image.removeDirectory(url)
        elif '' == file and '' == subfolder:
            url = image.get_upload_dir() . folder . '/'
            if (file_exists(url)) {
                image.removeDirectory(url)
            }
        } else {
            recortes = image.get_recortes(folder)
            if ('' != subfolder) {
                subfolder .= '/'
            }
            if ('' != sub) {
                sub .= '/'
            }
            url = image.get_upload_dir() . folder . '/' . subfolder . sub . file['url']
            if (file_exists(url)) {
                unlink(url)
            }

            foreach (recortes as key => recorte) {
                url = image.get_upload_dir() . folder . '/' . subfolder . sub . image.nombre_archivo(file['url'], recorte['tag'])
                if (file_exists(url)) {
                    unlink(url)
                }

                url = image.get_upload_dir() . folder . '/' . subfolder . sub . image.nombre_archivo(file['url'], recorte['tag'], 'webp')

                if (file_exists(url)) {
                    unlink(url)
                }

            }
        }
    }