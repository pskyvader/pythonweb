from core.view import view
from core.app import app


class footer:
    def normal(self):
        ret = {'body': ''}
        if app.post.getfirst("ajax") is None:
            ret['body'] = view.render('footer')
            ret['body']+=view.js()
        return ret