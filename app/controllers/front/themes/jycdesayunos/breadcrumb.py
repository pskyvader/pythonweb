from core.functions import functions


from app.models.seo import seo as seo_model


class breadcrumb:
    def normal(breadcrumb=[]):
        seo=seo_model.getById(1)
        b = [
            {'url' : functions.generar_url(array(seo['url'])), 'title' :seo['titulo']},
        ]
        b=b+breadcrumb
        foreach (b as key : bread) {
            b[key]['is_active']=false
            b[key]['active']=''
        }
        last=array_pop(b)
        last['is_active']=true
        last['active']='active'
        b[]=last

        view.set('breadcrumb', b)
        last=array_pop(b)
        view.set('titulo', last['title'])
        if(count(b)>1){
            last=array_pop(b)
            view.set('subtitulo', last['title'])
            view.set('is_subtitulo', true)
        }else{
            view.set('subtitulo', '')
            view.set('is_subtitulo', false)
        }
        view.render('breadcrumb')
    }
