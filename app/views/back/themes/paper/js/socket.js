
websocket=null
function log_socket(){
    ws=path.replace("https", "ws");
    ws=ws.replace("http", "ws");
    websocket = new WebSocket(path + ":5678/");
    console.log(websocket);
    websocket.onmessage = function(event) {
        data=event.data
        console.log(data);
        notificacion_footer('SOCKET: ' + data + ' ');
    };
}
function close_socket(){
    websocket=null
}