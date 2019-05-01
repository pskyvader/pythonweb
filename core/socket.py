
from websocket import create_connection

class socket:
    sock = None
    host = "ws://socket.mysitio.cl:8000/ws"
    @staticmethod
    def send(msg):
        if socket.sock==None:
            socket.sock = create_connection(socket.host)
        socket.sock.send(msg)
    @staticmethod
    def close():
        if socket.sock!=None:
            socket.sock.close()
            socket.sock=None
        

