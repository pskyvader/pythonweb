from core.view import view
from os.path import splitext
from pathlib import Path


def init(var):
    h = static()
    ret = h.index(var)
    return ret


class static:
    def index(self, var):
        ret = {'body': ''}
        theme = view.get_theme()
        resource = '/'.join(var)
        return ret
