var ws = new WebSocket("ws://" + path + ":5678/");
ws.onmessage = function(event) {
    data=event.data
    notificacion_footer('SOCKET: ' + data + ' ');
};