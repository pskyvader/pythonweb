
websocket=null
function log_socket(){
    ws=path.replace("https", "ws");
    ws=ws.replace("http", "ws");
    ws=ws.replace("admin/", "");
    websocket = new WebSocket(ws + ":80/hello-tornado");
    console.log(websocket);
    websocket.onmessage = function(event) {
        data=event.data
        console.log(data);
        notificacion_footer('SOCKET: ' + data + ' ');
    };
}
function close_socket(){
    websocket.close_socket()
    websocket=null
}