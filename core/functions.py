import os
def current_url():
    url = os.environ['HTTP_HOST']
    uri = os.environ['REQUEST_URI']
    return url + uri