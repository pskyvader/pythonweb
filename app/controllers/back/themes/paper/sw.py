from core.app import app
from core.functions import functions
from core.view import view
class sw():
    def init(self,var=[]):
        ret={'body':[]}

        version_application=1
        config = app.get_config()

        lista_cache = []
        lista_cache.append(functions.generar_url(["application","index",version_application], False))
        
        #array(css,fecha modificacion mas reciente)
        css = view.css(True, True) 
        #array(js,fecha modificacion mas reciente)
        js = view.js(True, True)
        
        foreach (css[0] as key => c) {
            lista_cache[] = c['url']
        }
        foreach (js[0] as key => j) {
            lista_cache[] = j['url']
        }
        
        
        view.set('lista_cache',functions.encode_json(lista_cache))
        view.set('cache',True)
        view.set('version',js[1].'-'.css[1])
        header('Content-Type: application/javascript')
        view.render('sw',False)


        return ret