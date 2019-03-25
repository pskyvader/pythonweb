websocket = null

function log_socket() {
    ws = path.replace("https", "ws");
    ws = ws.replace("http", "ws");
    ws = ws.replace("/admin/", "");
    websocket = new WebSocket(websocket_url);
    websocket.onopen = function(event) {
        websocket.send("Hello, world");
        setTimeout(() => {
            websocket.send("Hello 2");
        }, 3000);
    };
    websocket.onmessage = function(event) {
        data = event.data
        console.log(data);
        notificacion_footer('SOCKET: ' + data + ' ');
    };
    window.onbeforeunload = function() {
        if (websocket != null) {
            websocket.onclose = function() {};
            websocket.close();
            websocket = null
        }
    };
}

function close_socket() {
    //console.log('cerrar socket');
    if (websocket != null) {
        websocket.close();
        websocket = null;
    }
}