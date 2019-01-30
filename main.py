#import cgitb
#cgitb.enable()
def init():
    view.add('hola','hello world')
    return view.render()

class view:
    data = {}
    @staticmethod
    def add(key,value):
        view.data[key]=value
    @staticmethod
    def render():
        data_return=[]
        for key, value in view.data.items():
            a='<div>'+key+':'+value+'</div>'
            data_return.append(a)
        else:
            pass
        body='<br/>'.join(data_return)
        return body