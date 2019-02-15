from core.view import view
from core.app import app


class footer:
    def normal(self):
        ret = {'body': ''}
        if app.post.getfirst("ajax") is None:
            view.add('js',view.js())
            ret['body'] = view.render('footer')
        return ret