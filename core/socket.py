
from websocket import create_connection

class socket:
    sock = None
    host = "ws://socket.mysitio.cl:8000/ws"
    url="http://socket.mysitio.cl"
    intento=False

    @staticmethod
    def send(msg):
        try:
            if socket.sock==None:
                socket.sock = create_connection(socket.host)
            socket.sock.send(msg)
        except Exception:
            socket.sock=None
            if not socket.intento:
                socket.intento=True
                socket.create()


    @staticmethod
    def create():
        import urllib.request
        url=socket.url
        try:
            response = urllib.request.urlopen(url,timeout:100)
        except:
            pass

    @staticmethod
    def close():
        if socket.sock!=None:
            socket.sock.close()
            socket.sock=None
        

