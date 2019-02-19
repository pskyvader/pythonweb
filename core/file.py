from .image import image
class file(image):
    @classmethod
    def delete(cls,folder, file = '', subfolder = '', sub = ''):
        if "" == file and '' != subfolder:
            url = cls.get_upload_dir() + folder + '/' + subfolder + '/'
            if (file_exists(url)) {
                cls.removeDirectory(url)
            }
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