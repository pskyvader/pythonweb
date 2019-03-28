from core.app import app
from core.cache import cache
from core.image import image
from app.models.logo import logo as logo_model



class favicon:
    def init(self, var):
        logo=logo_model.getById(1)
        theme =  app.get_dir(True)+'uploads/'
        resource_url = image.generar_dir(logo['foto'][0], 'favicon')
        resource = resource_url[len(theme):]
        ret=cache.serve_cache(resource_url,theme,resource)
        return ret
