from pathlib import Path
from .image import image


class file(image):
    types = ["application/zip", "application/x-zip-compressed", "application/octet-stream", "application/postscript", "application/msword", "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.openxmlformats-officedocument.spreadsheetml.template", "application/vnd.openxmlformats-officedocument.presentationml.template", "application/vnd.openxmlformats-officedocument.presentationml.slideshow",
             "application/vnd.openxmlformats-officedocument.presentationml.presentation", "application/vnd.openxmlformats-officedocument.presentationml.slide", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template", "application/vnd.ms-excel.addin.macroEnabled.12", "application/vnd.ms-excel.sheet.binary.macroEnabled.12", "application/pdf", "application/download"]
    extensions = ["zip", "doc", "docx", "dotx", "xls", "xlsx", "xltx",
                  "xlam", "xlsb", "ppt", "pptx", "potx", "ppsx", "sldx", "pdf"]

    @classmethod
    def delete(cls, folder, file='', subfolder='', sub=''):
        import shutil
        if "" == file and '' != subfolder:
            url = cls.get_upload_dir() + folder + '/' + subfolder + '/'
            my_file = Path(url)
            if my_file.is_dir():
                shutil.rmtree(url)
        elif '' == file and '' == subfolder:
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
                subfolder + sub + file['url']
            my_file = Path(url)
            if my_file.is_file():
                my_file.unlink()
