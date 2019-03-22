
websocket=null
function log_socket(){
    websocket = new WebSocket("ws://" + path + ":5678/");
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