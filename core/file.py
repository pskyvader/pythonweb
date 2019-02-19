from pathlib import Path
from .image import image
class file(image):
    @classmethod
    def delete(cls,folder, file = '', subfolder = '', sub = ''):
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
            
            if ('' != sub) {
                sub .= '/'
            }
            url = cls.get_upload_dir() . folder . '/' . subfolder . sub . file['url']
            if (file_exists(url)) {
                unlink(url)