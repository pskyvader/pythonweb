from core.view import view
from core.app import app


class footer:
    def normal(self):
        ret = {'body': ''}
        if 'ajax' not in app.post:
            view.add('js',view.js())
            ret['body'] = view.render('footer')
        return ret