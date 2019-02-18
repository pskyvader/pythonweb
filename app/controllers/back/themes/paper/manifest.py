def init(var):
    h = manifest()
    if 0 in var:
        del var[0]
    ret = h.index(var)
    return ret

class manifest:
    def index(self):
        ret = {'body':''}
        return ret