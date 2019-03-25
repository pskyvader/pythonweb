
websocket=null
function log_socket(){
    ws=path.replace("https", "ws");
    ws=ws.replace("http", "ws");
    ws=ws.replace("admin/", "");
    websocket = new WebSocket(ws + "websocket");
    console.log(websocket);
    websocket.onmessage = function(event) {
        data=event.data
        console.log(data);
        notificacion_footer('SOCKET: ' + data + ' ');
    };
}
function close_socket(){
    console.log('cerrar socket');
    websocket.close_socket()
    websocket=null
}