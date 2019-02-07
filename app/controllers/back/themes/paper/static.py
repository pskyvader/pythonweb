
def init(var):
    h = static()
    ret = h.index(var)
    return ret



class static:
    url = ['home']
    metadata = {'title': 'Home', 'modulo': 'home'}

    def index(self,var):
        ret = {'body':''}
        url_return=functions.url_redirect(self.url)
        if url_return!='':
            ret['error']=301
            ret['redirect']=url_return
            return ret
        
        h = head(self.metadata)
        ret_head=h.normal()
        if ret_head['headers']!='':
            return ret_head
        ret['body']+=ret_head['body']
        
        he=header()
        ret_header=he.normal()
        ret['body']+=ret_header['body']

        asi = aside()
        ret_asi=asi.normal()
        ret['body']+=ret_asi['body']


        view.add('title', 'index')
        view.add('var', str(app.post.getfirst("ajax")))
        breadcrumb=[
            {'active':'active','url':'aaaa','title':'titulo'},
            {'active':'','url':'bbb','title':'titulo2'},
            {'active':'active','url':'ccc','title':'titulo3'},
        ]
        view.add('breadcrumb', breadcrumb)
        ret['body'] += view.render('home')


        f = footer()
        ret_f=f.normal()
        ret['body']+=ret_f['body']

        return ret