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
        } elseif ('' == file && '' == subfolder) {
            url = cls.get_upload_dir() . folder . '/'
            if (file_exists(url)) {
                cls.removeDirectory(url)
            }
        } else {
            if ('' != subfolder) {
                subfolder .= '/'
            }
            if ('' != sub) {
                sub .= '/'
            }
            url = cls.get_upload_dir() . folder . '/' . subfolder . sub . file['url']
            if (file_exists(url)) {
                unlink(url)